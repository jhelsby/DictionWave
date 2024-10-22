from jellyfish import damerau_levenshtein_distance
import pybktree
from tqdm import tqdm

input_file = '../filtered_crawl-300d-2M.vec'
misspellings_file = "misspellings.txt"
misspellings_sample_file = "misspellings_sample.txt"
sample_size = 1000

# Compare the frequent_threshold most frequent words to the
# rareness_threshold most rare words. Hypothesise that
# any rare words that are too similar to the most 
# frequent words are likely misspellings of the frequent word.
frequent_threshold = 100000
rareness_threshold = 100000

with open(input_file, 'r', encoding='utf-8') as f_in, open(misspellings_file, 'w', encoding='utf-8') as f_out:
    """
    Create a new word vector file, filtering out all unwanted words.
    """

    print(f"Filtering embeddings from {input_file}.")

    total_words = 1239471

    most_frequent_words = []
    rarest_words = []

    # Use tqdm to create a progress bar
    for i, line in enumerate(tqdm(f_in, total=total_words, desc=f"Reading the {frequent_threshold} most frequent words", unit="line")):
        if frequent_threshold < i < total_words - rareness_threshold:
            continue

        # Word is first space separated element in line.
        word = line.split()[0].lower()

        if i <= frequent_threshold:
            most_frequent_words.append(word)
        else:
            rarest_words.append(word)

    print("Building BK-tree of most-frequent words...")

    tree = pybktree.BKTree(damerau_levenshtein_distance, most_frequent_words)

    print("Finished building BK-tree.")

    misspellings = 0
    # Search for similar words (distance <= 1) in the rare words list
    for word in tqdm(rarest_words, total=rareness_threshold, desc=f"Filtering the {rareness_threshold} rarest words for possible misspellings", unit="word"):
        close_matches = tree.find(word, 1)
        if close_matches:
            f_out.write(f"{word}\n")
            misspellings += 1
    
    print(f"{misspellings} possible misspellings found.")