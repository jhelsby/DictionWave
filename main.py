import numpy as np
from tqdm import tqdm
import random

embeddings_file = "filtered_crawl-300d-2M.vec"

# Number of lines in my filtered_crawl-300d-2M.vec file - precomputed.
total_number_of_words = 1327177

word_vectors = dict()
word_ranks = dict()
lowercase_to_upper = dict()

num_words_to_output = 200

# Function to load the top number_of_words word vectors from the .vec file
def load_embeddings(number_of_words):

    with open(embeddings_file, 'r', encoding='utf-8') as f:
        # Skip the first line with metadata
        next(f)

        progress_bar = tqdm(total=number_of_words, desc="Loading embeddings", unit="lines")
        
        for i, line in enumerate(f):
            if i >= number_of_words:
                break
            
            tokens = line.rstrip().split(' ')
            word = tokens[0]
            lowercase = word.lower()
            lowercase_to_upper[lowercase] = word
            vector = np.asarray(tokens[1:], dtype='float32')
            word_vectors[lowercase] = vector
            word_ranks[lowercase] = i  # Store the index as rank
            
            progress_bar.update(1)
        
        progress_bar.close()
    

# Function to compute cosine similarity between two vectors
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Function to apply rarity boost to similarity score
def apply_rarity_boost(similarity, word_rank, max_rank, rarity_boost):
    # Apply the rarity boost based on the word's rank
    rarity_weight = 1 + rarity_boost * (word_rank / max_rank)
    return similarity * rarity_weight

# Function to find the most similar words both with and without rarity bias
def most_similar(word, rarity_boost=5.0, randomness=0.0):

    if word not in word_vectors:
        print(f"{word} not found. Please try another word.")
        return [], []
    
    word_vector = word_vectors[word]
    similarities = {}
    boosted_similarities = {}
    
    # Get the highest rank for normalization
    max_rank = max(word_ranks.values())  

    # Get the number of words to shuffle for randomness
    shuffle_length = num_words_to_output + int(randomness * num_words_to_output)

    for other_word, other_vector in word_vectors.items():
        if other_word != word:
            # Calculate pure cosine similarity
            similarity = cosine_similarity(word_vector, other_vector)
            similarities[other_word] = similarity
            
            # Calculate boosted similarity with rarity boost applied
            rank = word_ranks[other_word]
            boosted_similarity = apply_rarity_boost(similarity, rank, max_rank, rarity_boost)
            boosted_similarities[other_word] = boosted_similarity
    
    # Sort both pure similarities and boosted similarities
    most_similar_words = sorted(similarities.items(), key=lambda item: item[1], reverse=True)[:shuffle_length]
    most_similar_words_boosted = sorted(boosted_similarities.items(), key=lambda item: item[1], reverse=True)[:shuffle_length]

    random.shuffle(most_similar_words)
    random.shuffle(most_similar_words_boosted)
    
    return most_similar_words[:num_words_to_output], most_similar_words_boosted[:num_words_to_output]

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

    embeddings = load_embeddings(number_of_words)

    # Prompt user
    print((f"How many words would you like to be shown with each query? Default is 200."))
    num_words_to_output = interpret_user_input(input(f"Number of words to see: "), int, 200)

    # Prompt user
    print((f"Enter a rarity boost factor. 0 for no boost, higher values favor rare words. Default value is 5.0. If you enter 0, no rarity-boosted words will be shown."))
    rarity_boost = interpret_user_input(input("Rarity boost: "), float, 5.0)

    # Prompt user
    print("Enter a randomness factor. 0 for no randomness, higher values introduce randomness. Default value is 0.0.")
    randomness = interpret_user_input(input("Randomness factor:"), float, 0.0)

    print(f"You have selected {number_of_words} words, a rarity boost of {rarity_boost}, and a randomness factor of {randomness}. Have fun!\n")

    while True:
        word = input("Enter a word: ").lower()
        print()
        if word == "":
            print("Please enter a word.\n")
            continue

        most_similar_words, most_similar_boosted = most_similar(word, rarity_boost=rarity_boost, randomness=randomness)

        if not most_similar_words:
            continue

        print("Most similar words:\n")
        for word, _ in most_similar_words:
            print(lowercase_to_upper[word], end=" ")

        print("\n")
        if rarity_boost != 0.0:
            print("Rarity boosted words:\n")

            for word, _ in most_similar_boosted:
                print(lowercase_to_upper[word], end=" ")

            print("\n")

