import numpy as np
from tqdm import tqdm
import random

embeddings_file = "filtered_crawl-300d-2M.vec"

# Number of lines in my filtered_crawl-300d-2M.vec file - precomputed.
total_number_of_words = 1240641

# Function to load the top number_of_words word vectors from the .vec file
def load_embeddings(number_of_words):

    if number_of_words is None:
        number_of_words = total_number_of_words

    with open(embeddings_file, 'r', encoding='utf-8') as f:
        # Skip the first line with metadata
        next(f)

        lowercase_word_to_index = dict()
        lowercase_word_to_word = dict()

        lowercase_words = []
        nparray_vectors_list = []

        for i, line in tqdm(enumerate(f), total=number_of_words, desc="Loading embeddings", unit="lines"):
            if i >= number_of_words:
                break
            
            word, *vector = line.rstrip().split(' ')
            
            lowercase_word = word.lower()
            lowercase_words.append(lowercase_word)
            lowercase_word_to_word[lowercase_word] = word
            lowercase_word_to_index[lowercase_word] = i

            nparray_vectors_list.append(np.asarray(vector, dtype='float32'))      

    word_vectors = np.stack(nparray_vectors_list)
    word_list = np.array(lowercase_words)

    return word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word

# Function to compute cosine similarity between a vector and all word vectors
def cosine_similarity(query_vector, vectors):
    dot_products = np.dot(vectors, query_vector)
    norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    return dot_products / norms

# Function to apply rarity boost to all similarities
def apply_rarity_boost(similarities, rarity_boost):

    number_of_words = len(similarities)

    # Words are in descending order of frequency. The most common word has a
    # rareness of 0, and the least common has a rareness of 1.
    word_rareness = np.arange(number_of_words) / number_of_words - 1

    rarity_weights = 1 + rarity_boost * word_rareness

    return similarities * rarity_weights

# Function to find the most similar words both with and without rarity boost
def most_similar(word, word_list, word_vectors, lowercase_word_to_index, rarity_boost=5.0, randomness=0.0, num_words_to_output=200):

    word_index = lowercase_word_to_index.get(word)

    if word_index is None:
        print(f"{word} not found. Please try another word.")
        return [], []
    
    word_vector = word_vectors[word_index]

    similarities = cosine_similarity(word_vector, word_vectors)
   
    boosted_similarities = apply_rarity_boost(similarities, rarity_boost)
    
    # The larger the randomness factor, the more words we consider including in the output.
    shuffle_length = num_words_to_output + int(randomness * num_words_to_output)
    
    # Get the indices of the top 'shuffle_length' most similar words
    most_similar_idx = np.argsort(similarities)[::-1][:shuffle_length]
    most_similar_boosted_idx = np.argsort(boosted_similarities)[::-1][:shuffle_length]
    
    # SHuffle these words
    random.shuffle(most_similar_idx)
    random.shuffle(most_similar_boosted_idx)
    
    # Select the top 'num_words_to_output' from the shuffled indices
    most_similar_words = [word_list[i] for i in most_similar_idx[:num_words_to_output]]
    most_similar_words_boosted = [word_list[i] for i in most_similar_boosted_idx[:num_words_to_output]]
    
    return most_similar_words, most_similar_words_boosted

def interpret_user_input(input, data_type_func, default):
    """
    Given a user input, convert it into the appropriate datatype,
    or return a default value if no input was provided.
    """
    if input == "":
        return default

    return data_type_func(input)

# Main program
if __name__ == "__main__":
    
    # Prompt user
    print((f"Enter the number of words to load. Leave blank if you want to load all {total_number_of_words} words."))
    number_of_words = interpret_user_input(input(f"Number of words to load: "), int, total_number_of_words)

    word_list, word_vectors, lowercase_word_to_index, lowercase_word_to_word = load_embeddings(number_of_words)

    # Prompt user
    print((f"How many words would you like to be shown with each query? Default is 200."))
    num_words_to_output = interpret_user_input(input(f"Number of words to see: "), int, 200)

    # Prompt user
    print((f"Enter a rarity boost factor. 0 for no boost, higher values favor rare words. Negative values will show common words more often. \nDefault value is 5.0. If you enter 0, no rarity-boosted words will be shown."))
    rarity_boost = interpret_user_input(input("Rarity boost: "), float, 5.0)

    # Prompt user
    print("Enter a randomness factor. 0 for no randomness, higher values introduce randomness. Default value is 0.0.")
    randomness = interpret_user_input(input("Randomness factor:"), float, 0.0)

    randomness = 0. if randomness < 0 else randomness

    print(f"You have selected {number_of_words} words, a rarity boost of {rarity_boost}, and a randomness factor of {randomness}. Have fun!\n")

    while True:
        word = input("Enter a word: ").lower()
        print()
        if word == "":
            print("Please enter a word.\n")
            continue

        most_similar_words, most_similar_boosted = most_similar(word, word_list, word_vectors, lowercase_word_to_index, rarity_boost=rarity_boost, randomness=randomness)

        if not most_similar_words:
            continue

        print("Most similar words:\n")
        for word in most_similar_words:
            print(lowercase_word_to_word[word], end=" ")

        print("\n")
        if rarity_boost != 0.0:
            print("Rarity boosted words:\n")

            for word in most_similar_boosted:
                print(lowercase_word_to_word[word], end=" ")

            print("\n")