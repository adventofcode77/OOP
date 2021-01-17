import wiktionary_de_parser
from wiktionary_de_parser import Parser
import random

file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'

def iterate(record):
    dict = {"bedeutungen":[],"trennung":[record["syllables"]]}
    #print(record)
    #print(record.keys())
    text1 = record["wikitext"].replace("{{","")
    text1 = text1.replace("}}","")
    text1 = text1.replace("[[","")
    text1 = text1.replace("]]","")
    text1 = text1.split("\n\n")
    #print(text1)
    for i in range(len(text1)):
        line = text1[i].split("\n")
        #print(line)
        if line[0] == "Bedeutungen":
            for j in range(1,len(line)):
                dict["bedeutungen"].append(line[j])
    return dict

listofrecords = []
#parseddict = open("parsed_dict","w")
for record in Parser(file_path):
    #print(record)
    listofrecords.append(record)
    #parseddict.write(str(record))
    if len(listofrecords) == 1000:
         break
#parseddict.close()

print(len(listofrecords))


def getaword():
    j = random.randrange(0,1000)
    record = listofrecords[j]
    if 'langCode' not in record or record['langCode'] != 'de':
        return getaword()
    # do stuff with 'record'
    dict = iterate(record)
    return record["title"],dict

def getsilben(record):
    liste = []
    #print(record)
    #print(record.keys())
    text1 = record["wikitext"].replace("{{","")
    text1 = text1.replace("}}","")
    text1 = text1.replace("[[","")
    text1 = text1.replace("]]","")
    text1 = text1.split("\n\n")
    print(text1)
    for i in range(len(text1)):
        line = text1[i].split("\n")
        #print(line)
        if line[0] == "Bedeutungen":
            for j in range(1,len(line)):
                dict["bedeutungen"].append(line[j])
    return dict

getsilben(getaword())

dictwords = {}
for i in range(10):
    string,dict = getaword()
    #print(dict)
    if len(dict["bedeutungen"]) == 1 and len(dict["bedeutungen"][0]) < 100:
        dictwords[string] = dict
        print(string,dictwords[string])
        break
