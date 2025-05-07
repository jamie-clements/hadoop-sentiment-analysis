#!/usr/bin/env python3
import sys
from collections import defaultdict
    
# Student ID: 3012792

"""
Reducer for sentiment analysis.
Identifies the top 5 most common words for each of the item types and sentiment combination.

Input: Aggregated counts from combiner in format "item_type_sentiment\tword\tcount"
Output: Top 5 words for each item_type and sentiment combination
"""

def main():
    """
    Main processing function for the reducer
    Reads in input from STDIN, aggregates word counts by item_type and sentiment,
    and outputs the top 5 words for each combination.
    """
    # Dictionary to store word counts for each type_sentiment combination
    # using nested defaultdict for efficent counting
    type_sentiment_words = defaultdict(lambda: defaultdict(int))

    # Process input from STDIN (from combiner)
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # parse the input from combiner
        try:
            key, word, count = line.split('\t')
            count = int(count)
        except ValueError:
            continue  # Skip malformed lines
        
        # Accumulate word counts for each type_sentiment
        type_sentiment_words[key][word] += count

    # For each type_sentiment combination, find top 5 words
    for key in sorted(type_sentiment_words.keys()):
        word_counts = type_sentiment_words[key]
        
        # Sort words by count (descending) and alphabetically for ties
        # then take the top 5
        top_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))[:5]
        
        # Split key back into type and sentiment
        try:
            review_type, sentiment = key.split('_')
        except ValueError:
            print(f"Error: Malformed key '{key}' - expected format 'type_sentiment'", file=sys.stderr)
            continue
        
        # Format output: type sentiment word1 word2 word3 word4 word5
        words = ' '.join(word for word, _ in top_words)
        print(f"{review_type} {sentiment} {words}")

if __name__ == "__main__":
    main()