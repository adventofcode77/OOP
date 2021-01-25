import wiktionary_de_parser
from wiktionary_de_parser import Parser
import random

file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'

def iterate(record):
    print(record)
    print(record.keys())
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
                    print("plus one ", line[i+1])
                    meaning = line[i+1].split(",")[0] #only the first meaning
    else:
        return False
    return meaning,record['syllables']

listofrecords = []
for record in Parser(file_path):
    #print(record)
    listofrecords.append(record)
    if len(listofrecords) == 1000:
        break

def getaword():
    j = random.randrange(0,1000)
    #print(j)
    record = listofrecords[j]
    #print(record["title"])
    #print(record)
    if 'langCode' not in record or record['langCode'] != 'de':
        return getaword()
    # do stuff with 'record'
    if iterate(record):
        bedeutung, syls = iterate(record)
        simplelistforaword = [record["title"],bedeutung, syls]
        print("returning the right thing ",simplelistforaword)
        return simplelistforaword
    else:
        return getaword()



def quick_get(num):
    dictwords = {}
    for i in range(num):
        print("what about me ",num,i)
        list = getaword()
        print("the list ",list)
        print("0th ",list[0])
        print("1st ",list[1])
        print("2nd ",list[2])
        dictwords[list[0]] = [list[1],list[2]]
    return dictwords
