# Hadoop Sentiment Analysis

A MapReduce implementation for analyzing sentiment patterns in product, movie, and restaurant reviews.

## Overview

This project uses Hadoop MapReduce to analyze review text data and identify the most common words associated with positive and negative sentiments across different item categories. It demonstrates efficient distributed text processing using the MapReduce paradigm.

## Features

- Processes reviews categorized by item type (Restaurant, Movie, Product)
- Identifies sentiment-specific vocabulary patterns
- Filters common words using an exclusion list
- Implements text normalization (lowercase, punctuation removal)
- Uses combiner optimization for efficient processing

## Components

### Mapper (`mapper-1.py`)

The mapper processes each review line:
- Takes tab-separated input (item_type, review_text, sentiment)
- Cleans and tokenizes the text
- Removes excluded words and punctuation
- Emits key-value pairs: `item_type_sentiment \t word \t 1`

```python
# Key mapper functionality
for word in words:
    word = clean_word(word)
    if word and not word.isdigit() and word not in excluded:
        key = f"{item_type}_{sentiment}"
        print(f"{key}\t{word}\t1")
```

### Combiner (`combiner-1.py`)

The combiner performs local aggregation to reduce network traffic:
- Aggregates word counts by key from a single mapper
- Reduces data transfer between map and reduce phases
- Maintains same key-value format as mapper output

```python
# Core combiner logic
if key == current_key:
    word_counts[word] = word_counts.get(word, 0) + count
else:
    for w, c in word_counts.items():
        print(f"{current_key}\t{w}\t{c}")
```

### Reducer (`reducer-1.py`)

The reducer generates the final results:
- Aggregates word counts from all mappers/combiners
- Identifies top 5 most frequent words for each category
- Outputs results in a structured format

```python
# Find top words for each category
for key in sorted(type_sentiment_words.keys()):
    word_counts = type_sentiment_words[key]
    top_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))[:5]
    # Output formatted results
    review_type, sentiment = key.split('_')
    words = ' '.join(word for word, _ in top_words)
    print(f"{review_type} {sentiment} {words}")
```

## Example Output

```
Movie 0 bad you all but just
Movie 1 its but you good one
Product 0 phone my you on have
Product 1 great phone my very good
Restaurant 0 food place be we but
Restaurant 1 good great food place service
```

## Input Data Format

The input data consists of tab-separated values with three fields:
```
[item_type] [review_text] [sentiment]
```

Example:
```
Restaurant I had a pretty satisfying experience.                 1
Movie      Some applause should be given to the "prelude".       1
Product    A must study for anyone interested poor design.       0
```

## Running the Project

### Prerequisites
- Hadoop environment (2.x or 3.x)
- Python 3.x

### Setup

1. Create HDFS directories:
   ```bash
   hdfs dfs -mkdir -p /user/username/sentiment_analysis/input
   ```

2. Upload data:
   ```bash
   hdfs dfs -put data/reviews.txt /user/username/sentiment_analysis/input/
   hdfs dfs -put data/excluded.txt /user/username/sentiment_analysis/input/
   ```

3. Set execute permissions on Python scripts:
   ```bash
   chmod +x mapper-1.py combiner-1.py reducer-1.py
   ```

### Execution

Run the MapReduce job:

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files mapper-1.py,combiner-1.py,reducer-1.py,excluded.txt \
  -mapper "python3 mapper-1.py" \
  -combiner "python3 combiner-1.py" \
  -reducer "python3 reducer-1.py" \
  -input /user/username/sentiment_analysis/input/reviews.txt \
  -output /user/username/sentiment_analysis/output
```

View results:
```bash
hdfs dfs -cat /user/username/sentiment_analysis/output/part-*
```

## Performance Optimization

The implementation uses a combiner to optimize performance by:
- Reducing the volume of data transferred between mappers and reducers
- Decreasing computational load on reducers
- Maintaining result accuracy while improving efficiency

## License

MIT License
