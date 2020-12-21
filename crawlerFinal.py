# ===============================
# AUTHORS: Joshua Barnett, Karly Disanto

# SUBMIT DATE: 11/19

# CLASS: AI

# PROF: JORGE

# SPECIAL NOTES: No special notes
# ===============================

import re
import requests
class Crawler:
    def __init__(self, root):
        self.root = root
        self.stack= []
        self.visited = []
        self.stack.append(root)
        self.total = 1
        self.writing()

    def writing(self):
        url = self.stack[0]
        r = requests.get(url)
        r.close()
        #only match lines in the string with href= (following any symbols) and then put those results in a list
        hrefmatch = re.compile(r"(href=.+)")
        htmlLine = hrefmatch.findall(r.text)
        urls = []
        self.visited.append(url)
        count = 1
        #remove href and the end of the html tags off string
        for i in htmlLine:
            hrefremove = i[6:]
            singOrDoub = i[5]
            indexQuote = hrefremove.index(singOrDoub)
            finalUrl = hrefremove[:indexQuote]
            urls.append(finalUrl)
        #adding the root to the urls that end with html and also keeping countof rel and abs urls
        for i in urls:
            if i.endswith("html"):
                if i[0] == "/" or i[0] == "#":
                    word = self.root+i+"/"
                    self.stack.append(word)
            else:
                pass
        sentence = self.tagFinder(r.text)
        with open("doc1.txt", "w", encoding ="utf8") as file:
            file.write(url+"\n")
            file.write(sentence)
        #this while loop is used to loop through the satck and repeat the above process
        #not allowing the program to request from a url that was already visited
        while len(self.stack)>0 and count <= 30:
            self.total += 1
            url = self.stack.pop()
            count +=1
            while url in self.visited:
                if len(self.stack)== 0:
                    break
                url = self.stack.pop()
            r = requests.get(url)
            r.close()
            hrefmatch = re.compile(r"(href=.+)")
            htmlLine = hrefmatch.findall(r.text)
            urls = []
            try:
                for i in htmlLine:
                    hrefremove = i[6:]
                    singOrDoub = i[5]
                    indexQuote = hrefremove.index(singOrDoub)
                    finalUrl = hrefremove[:indexQuote]
                    urls.append(finalUrl)
            except ValueError:
                pass
            for i in urls:
                if i.endswith("html") or i.endswith("/"):
                    if i.startswith("http") == False:
                        if i[0] == "/" or i[0] == "#":
                            word = self.root+i
                            if word in self.stack:
                                pass
                            else:
                                self.stack.append(word)
                        else:
                            if i in self.stack:
                                pass
                            else:
                                self.stack.append(i)
                else:
                    pass
            self.visited.append(url)
            #this will create the files with all the needed information to them
            with open("doc" + str(count)+".txt", "w", encoding ="utf8") as file:
                sentence = self.tagFinder(r.text)
                file.write(url+"\n")
                file.write(sentence)


    def tagFinder(self,values):
        allWords = []
        paramatch = re.compile(r"(<p[>|| ].*)")
        paragraphs = paramatch.findall(values)
        spanmatch = re.compile(r"(<span.*)")
        spantag = spanmatch.findall(values)
        headmatch = re.compile(r"(<h\d.*)")
        headtag = headmatch.findall(values)
        titematch = re.compile(r"(<t.*)")
        titletag = titematch.findall(values)
        #print(paragraphs)
        for i in paragraphs:
            if '</p>' in i:
                try:
                    rightcarrot = i.index('>') + 1
                    closingP = i[rightcarrot:]
                    leftcarrot = closingP.index('<')
                    finalP = closingP[:leftcarrot]
                    allWords.append(finalP.strip())
                except ValueError:
                    pass
        for i in spantag:
            if '</span>' in i:
                try:
                    rightcarrot = i.index('>') + 1
                    closingP = i[rightcarrot:]
                    leftcarrot = closingP.index('<')
                    finalP = closingP[:leftcarrot]
                    allWords.append(finalP.strip())
                except ValueError:
                    pass
        for i in headtag:
            try:
                rightcarrot = i.index('>') + 1
                closingP = i[rightcarrot:]
                leftcarrot = closingP.index('<')
                finalP = closingP[:leftcarrot]
                allWords.append(finalP.strip())
            except ValueError:
                pass
        for i in titletag:
            try:
                rightcarrot = i.index('>') + 1
                closingP = i[rightcarrot:]
                leftcarrot = closingP.index('<')
                finalP = closingP[:leftcarrot]
                allWords.append(finalP.strip())
            except ValueError:
                pass

        fileSentence = "\n"
        fileSentence=  fileSentence.join(allWords)
        return fileSentence
        




