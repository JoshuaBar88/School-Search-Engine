# ===============================
# AUTHORS: Joshua Barnett, Karly Disanto

# SUBMIT DATE: 12/04

# CLASS: AI

# PROF: JORGE

# SPECIAL NOTES: No special notes
# ===============================

import json

import math



from nltk.util import Index

class Retrive:



    def __init__(self, query):

        self.query = query 

        self.invertedIndex= {}

        with open('knowledge.json') as json_file:

            self.invertedIndex = json.load(json_file)

        self.weightHold = {}

        self.compare = {}

        self.queryWeight = []

        self.weights()

               



#getting the weights of the word in the query and the documents that contain those words

    def weights(self):

        wordByWord = self.query.split()

        counter = {}



        for i in wordByWord:

            if i in counter.keys():

                counter[i] += 1

            else:

                counter[i] = 1      

        all_values = counter.values()

        max_value = max(all_values)

        count = -1



        for i in wordByWord:
            if i in self.invertedIndex.keys():
                doc = self.docFreq(len(self.invertedIndex[i]))
            else:
                doc = 0

            self.queryWeight.append((counter[i]/max_value) * doc)



        for i in wordByWord:

            count +=1

            listHold = []
            if i in self.invertedIndex.keys():
                docNum = len(self.invertedIndex[i])
                listHold.append(self.invertedIndex[i])
            else:
                docNum = 0
                listHold.append([])
            

            self.termFreaq(listHold, docNum, wordByWord, i)

            

        self.cosine()



#gets the term frequency of the word

#term freq = # times term is in doc/# max term in doc

    def termFreaq(self,holder, docNum, listQuery, count):
        if len(holder) == 0:
            return 0
        whichWord = listQuery.index(count)

        for i in holder:

            for j in i:

                document = j[0]

                value = j[1]

                calculations = 0

                calculations = value/self.invertedIndex[document]

                docFrequency = self.docFreq(docNum)

                calculations = calculations * docFrequency

                if document in self.weightHold.keys():

                    self.weightHold[document][whichWord]= calculations

                else:

                    self.weightHold[document] = [0 for i in range(len(listQuery))]

                    self.weightHold[document][whichWord]= calculations



#doc frequency = # docs / # doc contain the term 

    def docFreq(self,docNum):

        calc = self.invertedIndex["total"]/docNum

        return math.log10(calc)



#gets the vector magnitudes and in turn the cosine similarity of query and document words

#multiplies the weight of the word in document * weight of the word in query (numerator)

#magnitude of the vector (document and query)= sqrt(weight^2 + weight2^2 + weight3^2.....)

#cosine similarity = cosine(weights multiplied/(magnitude query * magnitude doc))

    def cosine(self):

        finale = {} 

        insideQ = 0

        insideD = 0

        magDoc = None



        for i in self.queryWeight:

            insideQ += i**2

        magQuery = math.sqrt(insideQ)

        

        for i,j in self.weightHold.items():

            insideD = 0

            multiply = 1



            for x in range(len(j)):

                insideD += j[x]**2

                multiply += j[x] * self.queryWeight[x]



            magDoc = math.sqrt(insideD)

            finale[i] = multiply/(magQuery * magDoc)


#sorts the results of the cosine similarity       

        linksSort = sorted(finale.items(), key = lambda kv:kv[1], reverse=True)

        self.bestLinks(linksSort)





#Gets the url from the first line in document and displays the sorted link urls

    def bestLinks(self, linksSorted):

        urls = []

        for i in range(10):

            try:

                f = open("doc" + str(linksSorted[i][0]) + ".txt", "r")

                url = f.readline()

                urls.append(url.strip())

            except IndexError:

                break

        print(urls)