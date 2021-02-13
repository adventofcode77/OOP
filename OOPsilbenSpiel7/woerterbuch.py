import wiktionary_de_parser
from wiktionary_de_parser import Parser
import random
import globale_variablen
import re

class Woerterbuch(globale_variablen.Settings):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.listofrecords = []
        self.list_records()
        self.parsed = self.quick_get(3)

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
                        #print("meanings for",record['title'])
                        meaning = line[i+1]
                        # for j in range(i+1,len(line)-1):
                        #     print(line[j])
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
        result = self.iterate(record)
        if result:
            bedeutung, syls = result
            simplelistforaword = [record["title"],bedeutung, syls]
            return simplelistforaword
        else:
            return self.getaword()



    def quick_get(self,num):
        dictwords = {}
        for i in range(num):
            success = False
            while not success:
                list = self.getaword()
                if "|" in list[1]:
                    continue
                list[1] = list[1][4:] # remove line number
                list[1] = re.sub('".*?"', '', list[1]) # copied how to remove quoted things
                list[1] = re.sub("''.*?''", '', list[1])
                list[1] = re.sub("<.*?>", '',list[1])
                list[1] = re.sub("[.*?]", '',list[1])
                #list[1] = re.sub("(.*?)", '', list[1]) # never finds such strings?
                if "Familienname" in list[1]:
                    continue
                if "Name" in list[1]:
                    continue
                if "Vorname" in list[1]:
                    continue
                if "Gemeinde in" in list[1]:
                    continue
                if len(list[1]) in range(3, 150):
                    success = True
                if "landschaftlich" in list[1]:  # geography cat
                    continue
                if len(list[1]) in range(3,150):
                    success = True
            #print("the list ",list)
            # print("0th ",list[0])  #word
            #print("1st ",list[1]) #meaning string
            # print("2nd ",list[2]) # syls
            dictwords[list[0]] = [list[1],list[2]]
        return dictwords

