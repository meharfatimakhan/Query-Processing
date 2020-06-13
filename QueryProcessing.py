# -*- coding: utf-8 -*-
import os
from nltk.stem import PorterStemmer
import timeit
import io

start = timeit.default_timer()

myQDict = {}

with open("query.txt","r+") as queryFile:
    query = set(queryFile.readlines()[0:])
queryFile.close()

for term in query:
    index = term.split()
    if index:
        myQDict[index[0]] = index[1:]

for i in myQDict:
    if type(myQDict[i]) is list:
        myQDict[i] = [j.lower() for j in myQDict[i]]
    else:
        myQDict[i] = myQDict[i].lower()
    
with io.open("C:\\Users\\Dell\\Downloads\\IR\\StopWords.txt","r", encoding="utf8") as f:
    stopwords = [word for line in f for word in line.split()]

porter = PorterStemmer()

def stemSentence(sentence):
    i = 0
    for word in sentence:
        sentence[i] = porter.stem(word)
        i = i + 1      
    return sentence

for qid, value in myQDict.items():
    filtered_query = []
    for w in value: 
        if w not in stopwords: 
            filtered_query.append(w) 
            myQDict[qid] = filtered_query
    myQDict[qid] = stemSentence(value)
            
del query
del stopwords

with open("termids.txt","r+") as termFile:
    termList = list(termFile.readlines()[0:])
termFile.close()

allTerms = {}
for t in termList:
    data = t.split("\t") 
    data[1] = data[1].strip() 
    allTerms[data[1]] = data[0]

del termList

for qids, values in myQDict.items():
    j = 0
    for word in values:
        ids = allTerms.get(word)
        if ids is not None: 
            values[j] = word.replace(word, ids)
            j = j + 1
        
del allTerms

with open("term_index.txt","r+") as termIndexFile:
    termIndexList = set(termIndexFile.readlines()[0:])
termIndexFile.close()

terms = {}

for t in termIndexList:
    index = t.split(" ")
    terms[index[0]] = index[3:]
    
del termIndexList

newDict = {}
for queryIDs, queryValues in myQDict.items():
    mySet = set()
    for word in queryValues:
        docIDs = terms.get(word) 
        if (docIDs is not None):
            myDocKey = 0
            for word2 in docIDs:
                key = word2.split(',')
                if ((key[0] != '') and (key[0] != '\n')):
                    myDocKey = myDocKey + int(key[0]) ##Decoding the Delta Encoding
                    mySet.add(str(myDocKey))
    newDict[queryIDs] = mySet
    
print(newDict)
    
with open("docids.txt","r+") as docFile:
    docNameList = set(docFile.readlines()[0:])
docFile.close()

docs = {}

for d in docNameList:
    docNames = d.split("\t")
    docs[docNames[0]] = docNames[1].strip()   
#del docNameList

for queryIDs, queryValues in newDict.items():
    for term in queryValues:
        docName = docs.get(term)
        if docName is not None: 
            queryValues.remove(term) 
            queryValues.add(docName)
              
f = open("my_output.txt", "w+", encoding="utf-8")
for queryIDs, queryValues in sorted(newDict.items()):
    f.writelines(queryIDs + " " + term + "\n" for term in queryValues)
f.close()

############ Calculating Performance ###################
with open("output.txt", "r+")  as outputFile2:
    actualOutput = list(outputFile2.readlines()[0:])
outputFile2.close()

actual_output = {}
checkIndex = []
for term in actualOutput:
    index3 = term.split()
    if index3[1].strip() in docs.values():
        if index3[0] in checkIndex:
            myval=index3[1].strip()
            actual_output[index3[0]].add(myval)
        else:
            actual_output[index3[0]] = {index3[1].strip()}
            checkIndex.append(index3[0])


accuracyAvg=0
recallAvg=0
precAvg=0
f = open("performance.txt", "w+", encoding="utf-8")
for queryLine in sorted(newDict):
    queryLineIndex = queryLine.split()
    calcTruePositive = actual_output[queryLineIndex[0]].intersection(newDict[queryLineIndex[0]])
    truePositive = len(calcTruePositive)
    calcFalsePositive = newDict[queryLineIndex[0]] - actual_output[queryLineIndex[0]]
    falsePositive = len(calcFalsePositive)
    calcFalseNegative = actual_output[queryLineIndex[0]] - newDict[queryLineIndex[0]]
    falseNegative = len(calcFalseNegative)
    trueNegative = len(docNameList) - (truePositive + falsePositive + falseNegative)
    accuracy = (truePositive + trueNegative) /(truePositive + trueNegative + falsePositive + falseNegative)
    accuracyAvg = accuracy + accuracyAvg
    precision = truePositive /(truePositive + falsePositive)
    precAvg = precAvg + precision
    recall = truePositive /(truePositive + falseNegative)
    recallAvg = recallAvg + recall
    #average = (accuracy + precision + recall)/ 3
    accuracy = format(accuracy, '.3f')
    precision = format(precision, '.3f')
    recall = format(recall,'.3f')
   # average = format(average, '.3f')
    f.write(queryLineIndex[0] + "\t" + accuracy + "\t" + precision + "\t" + recall  + "\n")
    
precAvg = (precAvg / len(newDict))
precAvg = format(precAvg, '.3f')
recallAvg = (recallAvg / len(newDict))
recallAvg = format(recallAvg, '.3f')
accuracyAvg = (accuracyAvg / len(newDict))
accuracyAvg = format(accuracyAvg, '.3f')
f.write("Results" + "\t" + accuracyAvg + "\t" + precAvg + "\t" + recallAvg  + "\n")
f.close()   

stop = timeit.default_timer()
print('Total Time:', (stop - start), 'seconds') 