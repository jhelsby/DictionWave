"""
Identify possible misspellings using the following algorithm:

1.  Compare the M most common words to the N rarest words. 
    Assume common words are more likely to be spelt correctly, 
   and rare words are more likely to be misspellings.

2.  For each rare word, return all common words which are a
    Damerau-Levenshtein distance of 1 step away.

3.  If any of these common words have a sufficient cosine similarity
    with the rare word, they may have the same semantic meaning,
    but the rare word is simply a misspelling of the common word.
    Write this to the misspellings file.
"""

from jellyfish import damerau_levenshtein_distance
import pybktree
from tqdm import tqdm
import numpy as np
from similarity_core import cosine_similarity

input_file = 'filtered_crawl-300d-2M.vec'
misspellings_file = "misspellings.txt"
sample_size = 1000

# Compare the frequent_threshold most frequent words to the
# rareness_threshold most rare words. Hypothesise that
# any rare words that are too similar to the most 
# frequent words are likely misspellings of the frequent word.
frequent_threshold = 200000
rareness_threshold = 200000

# The minimum similarity a rare word needs to have with a frequent word
# to be counted as a misspelling and filtered out. This number was
# determined empirically by looking at data, on the basis that a false positive
# (discarding a valid word) is worse than a false negative (keeping a misspelling)
# for this use case.
similarity_threshold = 0.35

with open(input_file, 'r', encoding='utf-8') as f_in:
    """
    Load desired words and vectors.
    """

    print(f"Filtering embeddings from {input_file}.")

    total_words = 1239471

    most_frequent_words = []
    rarest_words = []
    word_to_vec = dict()

    # Use tqdm to create a progress bar
    for i, line in enumerate(tqdm(f_in, total=total_words, desc=f"Reading the {frequent_threshold} most frequent words", unit="line")):
        if frequent_threshold < i < total_words - rareness_threshold:
            continue

        word, *vector = line.rstrip().split(' ')

        word_to_vec[word] = np.asarray(vector, dtype='float32')

        if i <= frequent_threshold:
            most_frequent_words.append(word)
        else:
            rarest_words.append(word)

print("Building BK-tree of most-frequent words...")

tree = pybktree.BKTree(damerau_levenshtein_distance, most_frequent_words)

print("Finished building BK-tree.")

misspellings = 0

with open(misspellings_file, 'w', encoding='utf-8') as f_out:
    """
    Identify potential misspellings and write them to file.
    """

    # Search for similar words (distance == 1) in the rare words list
    for word in tqdm(rarest_words, total=rareness_threshold, desc=f"Filtering the {rareness_threshold} rarest words for possible misspellings", unit="word"):
        close_matches = [match for distance, match in tree.find(word, 1)]
        word_vec = word_to_vec[word]

        max_sim = float('-inf')
        max_match = None

        for match in close_matches:
            match_vec = word_to_vec[match]

            if cosine_similarity(word_vec, match_vec) > 0.35:
                f_out.write(f"{word}\n")
                misspellings += 1
                break
    
print(f"{misspellings} possible misspellings found.")