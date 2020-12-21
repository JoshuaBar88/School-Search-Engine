# ===============================
# AUTHORS: Joshua Barnett, Karly, Phil

# SUBMIT DATE: 12/04

# CLASS: AI

# PROF: JORGE

# SPECIAL NOTES: Only grabbing text with tags <p> <span> <h1/2/3>
# ===============================

import re

import string 

import json

import nltk

from nltk.collections import LazyEnumerate

from nltk.stem import PorterStemmer 

from nltk.tokenize import word_tokenize 

class Cleaner:



    def __init__(self, length, query = None):

        if query == None:

            self.allWords = []

            self.values = ""

            self.stopWords = ["a", "an", "and","are","as","at","be","by","for","from","has","he","with"

                        ,"in","is","it","its","of","on","that","the","to","was","were","will"]

            self.invertedIndex = {}

            self.total =0

            self.readFiles(length)

        else:

            self.stopWords = ["a", "an", "and","are","as","at","be","by","for","from","has","he","with"

                        ,"in","is","it","its","of","on","that","the","to","was","were","will"]

            self.query = query

            self.stem(length)

        

#reading the files created by the crawler calls the stemming and inverted index to clean those files

    def readFiles(self,length):

        for i in range(1, length):

            self.total += 1

            f = open("doc"+ str(i)+".txt", encoding="latin-1") 

            url = f.readline

            self.values = f.readlines()

            f.close()

            self.stem(i)

        self.invertedIndex["total"] = self.total

        #writes inverted index to a json file to be accessed later in retrieval

        with open("knowledge.json", "w") as outfile:  

            json.dump(self.invertedIndex, outfile, indent=1)

        



#uses nltk library to stem the words in the documents created

#changes everything to loswer case, no numbers, no contractions....etc.

    def stem(self,numofDoc):

        if numofDoc != 0:

            words = []

            stem = PorterStemmer()

            for i in self.values:

                sentenceList = i.split()

                for j in sentenceList:

                    if re.match(r'[a-zA-Z]+', j):

                        if j.lower() not in self.stopWords:

                            shorten = stem.stem(j.strip())

                            shorten = shorten.lower()

                            res = re.sub(r'[^\w\s]', '', shorten)

                            words.append(res)

            self.invertedInde(words, numofDoc)

        else:

            stem = PorterStemmer()

            finalString = ""

            sentenceList = self.query.split()

            for i in sentenceList:

                if re.match(r'[a-zA-Z]+', i):

                    if i.lower() not in self.stopWords:

                        shorten = re.sub(r'[^\w\s]', '', i)

                        shorten = stem.stem(shorten)

                        shorten = shorten.lower()

                        finalString += shorten + " "

            self.query = finalString

        

#created the inverted index for every word in the documents created to be used later when given a query

#stored in a dictionary: key = word --> value = list of lists [[docNumber, # of occurances], [docNumber, # of occurances]....]etc

    def invertedInde(self, words, num):

        counter = {}

        for i in words:

            if i in counter.keys():

                counter[i] += 1

            else:

                counter[i] = 1

        all_values = counter.values()

        max_value = max(all_values)

        self.invertedIndex[str(num)] = max_value

        for i,j in counter.items():

            docList = [str(num),j]

            if i in self.invertedIndex.keys():

                self.invertedIndex[i].append(docList)

            else:

                self.invertedIndex[i] = []

                self.invertedIndex[i].append(docList) 