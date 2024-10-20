from tqdm import tqdm
import re

input_file = 'crawl-300d-2M.vec'
blacklist_file = 'blacklist.txt'
output_file = 'filtered_crawl-300d-2M.vec'

# Number of lines in crawl-300d-2M.vec - precomputed.
total_lines = 1999996

# Filter out duplicates.
seen_words = set()

# Store blacklisted words, in lowercase.
blacklist = set()

with open(blacklist_file, 'r') as file:
    """
    Populate blacklist set, in lowercase.
    """
    for line in file:
        # Blacklist file is multiple lines of space-separated words.
        words = line.strip().split(" ")
        lowercase_words = [word.lower() for word in words]
        blacklist.update(lowercase_words)

def is_not_blacklisted(word):
    """
    Filter out blacklisted words. Blacklisted set is stored as lowercase.
    """
    return not word.lower() in blacklist

def is_unseen(word):
    """
    Filter out duplicate words with varying upper-
    and lower-case. e.g. "TEST" and "test" should be
    considered duplicates.
    """
    word_lower = word.lower()
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

    return contains_english_letters and punctuation_letters.fullmatch(word) is None and letters_punctuation.fullmatch(word) is None and letters_punctuationnodash_letters.fullmatch(word) is None and sports_scores.fullmatch(word) is None and dates_and_scores.fullmatch(word) is None

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

    # Use tqdm to create a progress bar
    for line in tqdm(f_in, total=total_lines, desc="Processing lines", unit="line"):
        # Split the line into the word and its vector components
        parts = line.split()
        word = parts[0] 

        if is_valid_word(word):
            f_out.write(line)  
            num_of_output_lines += 1

print(f"Output file: {output_file}")
print(f"Number of words in output: {num_of_output_lines}")
print(f"Number of words filtered out: {total_lines - num_of_output_lines}")