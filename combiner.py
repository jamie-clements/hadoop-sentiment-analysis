#!/usr/bin/env python3

import sys
import string

# Student ID: 3012792

"""
Combiner for sentiment analysis.
This combines word counts for the same item_type, sentiment and word combinations to 
reduce data transfer to reducers.

Input: Key-value pairs from the mapper in the format "item_type_sentiment\tword\t1"
Output: Aggregated counts in format "item_type_sentiment\tword\ttotal_count"
"""

# Keeping track of counts per type_sentiment and word
current_key = None
word_counts = {}

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
    
    # Parse input from mapper
    try:
        key, word, count = line.split('\t')
        # convert count to integer
        count = int(count)
    except ValueError:
        continue  # Skip malformed lines
    
    # initalise current_key if this is the first line
    if current_key is None:
        current_key = key
    
    # If we're still on same key, accumulate counts
    if key == current_key:
        # add to existing count or initalise new word
        word_counts[word] = word_counts.get(word, 0) + count
    else:
        # Output accumulated counts for previous key
        for w, c in word_counts.items():
            print(f"{current_key}\t{w}\t{c}")
        
        # Reset for new key
        current_key = key
        word_counts = {word: count}

if current_key is not None:
    for word, count in word_counts.items():
        print(f"{current_key}\t{word}\t{count}") 