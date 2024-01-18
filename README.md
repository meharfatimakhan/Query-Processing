# Query-Processing

Extract relevant documents from the corpus for queries.

## Query Processing Steps

### Query Pre-Processing

1. Read all the queries and generate a tokenized dictionary for all the tokens in query tokens. The key of the dictionary is the Query-Id and the value at each key/index is the list of all the tokens in the query

2. Convert all the tokens into lowercase

3. Remove all the stop-words from the list

4. Stem all the tokens



### Query Results

1. Replace the list of all words with term-Ids

2. Read positional index from the filename term index.txt

3. Get the list of documents and positions for every term in terms dictionary

4. Execute the delta decoding of the list of documents of all the terms

5. Read the docIds file

6. Replace docIds with document names in the  dictionary 

7. Write the Results to the my_ouput.txt file
