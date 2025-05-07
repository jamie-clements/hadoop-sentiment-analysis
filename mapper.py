#!/usr/bin/env python3

import sys
import string
import re

# Student ID: 3012792

"""
Mapper for sentiment analysis.
Input: Tap-separatee lines which contains item_type, review_text, and sentiment value (0 or 1)
Output: Key-value pairs in the format "item_type_sentiment\tword\t1"
"""

# Load excluded words from file with error handling
excluded = set()
try:
    with open('excluded.txt', 'r') as f:
        words = f.read().lower().strip().split()
        excluded.update(words)
except Exception as e:
    print(f"Error loading excluded words: {e}", file=sys.stderr)

def clean_word(word):
    """
    Cleans a word by converting to lowercase, removing punctuation and digits.

    Args:
        word: The input word to clean
    Returns:
        The cleaned word string
    """
    # Convert to lowercase
    word = word.lower()
    # Remove any digits
    word = re.sub(r'\d', '', word)
    # Remove any remaining punctuation
    word = re.sub(r'[^\w\s]', '', word)
    return word.strip()

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue

    # Parse input line into its components   
    try:
        # Split into item_type, review_text, and sentiment (0 or 1)
        (item_type, review, sentiment) = line.split('\t')

        # validate sentiment value
        if sentiment not in ['0', '1']:
            print(f"Warning: Invalid sentiment value '{sentiment}' - skipping line", file=sys.stderr)
        
        # Process each word in the review
        words = review.split()
        for word in words:
            # Clean each word
            word = clean_word(word)

            # Skip empty words, numbers, and excluded words
            if word and not word.isdigit() and word not in excluded:
                # create key as item_type_sentiment
                key = f"{item_type}_{sentiment}"
                # emit key-value pair: item_type_sentiment, word, count(1)
                print(f"{key}\t{word}\t1")
                
    except ValueError as e:
        print(f"Error parsing line: {e}", file=sys.stderr)
        continue