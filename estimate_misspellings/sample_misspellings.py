"""
Extract a sample of estimated misspellings, for manual verification.
"""

import random

misspellings_file = 'misspellings.txt'
misspellings_sample_file = "sample_misspellings.txt"
sample_size = 1000

words = []
with open(misspellings_file, 'r', encoding='utf-8') as f_in, open(misspellings_sample_file, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        words.append(line.strip())

    random.shuffle(words)
    
    for word in words[:sample_size+1]:
        f_out.write(f"{word}\n")
