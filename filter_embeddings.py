"""
Filter an input word vector file to remove duplicate,
irrelevant, and blacklisted words. Save the output to a
new word vector file, and the embeddings to a pkl file.
"""

from tqdm import tqdm
import re
import save_embeddings
import unicodedata

input_file = 'crawl-300d-2M.vec'
blacklist_file = 'blacklist.txt'
misspellings_file = 'misspellings.txt'
output_file = 'filtered_crawl-300d-2M.vec'

# Number of lines in crawl-300d-2M.vec - precomputed.
total_lines = 1999996

# Filter out duplicates.
seen_words = set()

# Store blacklisted words, in lowercase.
blacklist = set()

def populate_blacklist(file_to_blacklist):
    """
    Populate the blacklist set with words from the specified file, in lowercase.
    Each line in the file should contain space-separated words.
    
    :param blacklist_file: Path to the file containing words to add to the blacklist.
    :param blacklist: Set to which the words will be added.
    """
    with open(file_to_blacklist, 'r') as file:
        for line in file:
            words = line.strip().split(" ")
            lowercase_words = [word.lower() for word in words]
            blacklist.update(lowercase_words)

populate_blacklist(blacklist_file)
populate_blacklist(misspellings_file)

def is_not_blacklisted(word):
    """
    Filter out blacklisted words. Blacklisted set is stored as lowercase.
    """
    return not word.lower() in blacklist

def is_unseen(word):
    """
    1. Filter out duplicate words with varying upper-
    and lower-case. e.g. "TEST" and "test" should be
    considered duplicates.

    2. Filter out unicode characters that look like the 
    standard alphabet but aren't. e.g. е instead of e.
    """
    normalized_word = unicodedata.normalize('NFKC', word)
    word_lower = normalized_word.lower()
    if word_lower not in seen_words:
        seen_words.add(word_lower)
        return True

    return False

def is_valid_regex(word):
    """
    - Filter out words that contain no English alphabet characters.
    - Filter out words that start or end with punctuation, as 
    these are likely duplicates of words without that punctuation.
    - Filter out words that have certain punctuation marks in the middle,
    as these may be chunks of sentences (e.g. "easily.Thanks").
    - Filter out strings of the form num-num or num-num-num, e.g. 2-1, 14-2-86.
    """
    contains_english_letters = any(char.isascii() and char.isalpha() for char in word)

    punctuation_letters = re.compile(r'[,.@!%-]+[a-zA-Z0-9]*')
    letters_punctuation = re.compile(r'[a-zA-Z0-9]*[,.@!%-]+')
    letters_punctuationnodash_letters = re.compile(r'[a-zA-Z0-9]+[.,@!%]+[a-zA-Z0-9]+')
    sports_scores = re.compile(r'[0-9]+-[0-9]+')
    dates_and_scores = re.compile(r'[0-9]+[./-][0-9]+[./-][0-9]+')
    www_domains = re.compile(r'www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\.*')
    common_tlds = re.compile(r'[a-zA-Z0-9-]+\.(?:com|net|org|gov|edu|io|co|info|biz|me|us|co.uk)\.*')
    three_or_more_repeated_chars = re.compile(r'\b\w*(?:(.)\1{2,})\w*\b')

    patterns = [
        punctuation_letters,
        letters_punctuation,
        letters_punctuationnodash_letters,
        sports_scores,
        dates_and_scores,
        www_domains,
        common_tlds,
        three_or_more_repeated_chars
    ]

    return contains_english_letters and all(pattern.fullmatch(word) is None for pattern in patterns)

def is_valid_word(word):
    """
    A word is valid if it passes the above filters.
    """
    return is_not_blacklisted(word) and is_unseen(word) and is_valid_regex(word) 


num_of_output_lines = 0

with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
    """
    Create a new word vector file, filtering out all unwanted words.
    """

    print(f"Filtering embeddings from {input_file}.")

    # Use tqdm to create a progress bar
    for line in tqdm(f_in, total=total_lines, desc="Processing lines", unit="line"):
        # Word is first space separated element in line.
        word = line.split()[0] 

        if is_valid_word(word):
            f_out.write(line)  
            num_of_output_lines += 1

print(f"Output file: {output_file}")
print(f"Number of words in output: {num_of_output_lines}")
print(f"Number of words filtered out: {total_lines - num_of_output_lines}")

print("Saving to embeddings.pkl...")
save_embeddings.main()