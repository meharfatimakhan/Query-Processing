# Query-Processing

Extract relevant documents from the corpus for queries.

## Query Processing Steps:

### Query Pre-Processing

•	Read all the queries and generate a tokenized Dictionary for all the tokens in a query tokens. The key of the dictionary is the Query-Id and the value at each key/ index is the list of all the tokens in the query

•	Then, convert all the tokens into lowercase

•	After that, remove all the stop-words from the list

•	Finally stem all the tokens


### Query Results

•	Replace the list of all the words with term-Ids

•	Read positional index from the filename term index.txt

•	Get the list of documents and positions for every term in terms dictionary

•	Execute the delta decoding of the list of documents of all the terms

•	Read the docIds file

•	Replace docIds with document names in the  dictionary 

•	Write the Results to the my_ouput.txt file
