import wiktionary_de_parser
from wiktionary_de_parser import Parser
import random
import globale_variablen

class Woerterbuch(globale_variablen.Settings):
    def __init__(self, file_path):
        self.file_path = file_path
        self.listofrecords = []
        self.list_records()
        self.parsed = self.quick_get(50)

    def iterate(self,record):
        meaning = ""
        if 'syllables' in record.keys():
            text1 = record["wikitext"].replace("{{","")
            text1 = text1.replace("}}","")
            text1 = text1.replace("[[","")
            text1 = text1.replace("]]","")
            text1 = text1.split("\n\n")
            for i in range(len(text1)):
                line = text1[i]
                line = line.split('\n')
                for i in range (len(line)):
                    newline = line[i]
                    if newline == "Bedeutungen":
                        meaning = line[i+1]
        else:
            return False
        return meaning,record['syllables']


    def list_records(self):
        for record in Parser(self.file_path):
            self.listofrecords.append(record)
            if len(self.listofrecords) == 1000:
                break

    def getaword(self):
        j = random.randrange(0,1000)
        record = self.listofrecords[j]
        if 'langCode' not in record or record['langCode'] != 'de':
            return self.getaword()
        if self.iterate(record):
            bedeutung, syls = self.iterate(record)
            simplelistforaword = [record["title"],bedeutung, syls]
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

