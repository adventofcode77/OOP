import wiktionary_de_parser
from wiktionary_de_parser import Parser
import random

class Parse:
    def __init__(self):
        self.file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'
        self.listofrecords = []
        self.list_records()

    def iterate(self,record):
        #print(record)
        #print(record.keys())
        meaning = ""
        if 'syllables' in record.keys():
            text1 = record["wikitext"].replace("{{","")
            text1 = text1.replace("}}","")
            text1 = text1.replace("[[","")
            text1 = text1.replace("]]","")
            text1 = text1.split("\n\n")
            #print(text1)
            for i in range(len(text1)):
                line = text1[i]
                #print("line ", line)
                line = line.split('\n')
                for i in range (len(line)):
                    newline = line[i]
                    #print("here2 ",newline)
                    if newline == "Bedeutungen":
                        #print("plus one ", line[i+1])
                        meaning = line[i+1]
        else:
            return False
        return meaning,record['syllables']

    def list_records(self):
        for record in Parser(self.file_path):
            #print(record)
            self.listofrecords.append(record)
            if len(self.listofrecords) == 1000:
                break

    def getaword(self):
        j = random.randrange(0,1000)
        #print(j)
        record = self.listofrecords[j]
        #print(record["title"])
        #print(record)
        if 'langCode' not in record or record['langCode'] != 'de':
            return self.getaword()
        # do stuff with 'record'
        if self.iterate(record):
            bedeutung, syls = self.iterate(record)
            simplelistforaword = [record["title"],bedeutung, syls]
            #print("returning the right thing ",simplelistforaword)
            return simplelistforaword
        else:
            return self.getaword()



    def quick_get(self,num):
        dictwords = {}
        for i in range(num):
            #print("what about me ",num,i)
            list = self.getaword()
            list[1] = list[1][4:]
            # print("the list ",list)
            # print("0th ",list[0])  #word
            # print("1st ",list[1]) #meaning string
            # print("2nd ",list[2]) # syls
            dictwords[list[0]] = [list[1],list[2]]
        return dictwords

