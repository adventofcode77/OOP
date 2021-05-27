# -*- coding: utf-8 -*-
import random
import re

#from wiktionary_de_parser import Parser

# ACTIVE MODE COMMENTED OUT

def iterate(record):
    meaning = ""
    if 'syllables' in record.keys():
        text1 = record["wikitext"].replace("{{", "")
        text1 = text1.replace("}}", "")
        text1 = text1.replace("[[", "")
        text1 = text1.replace("]]", "")
        text1 = text1.split("\n\n")
        for i in range(len(text1)):
            line = text1[i]
            line = line.split('\n')
            for i in range(0,len(line)):
                THE_NEXT_LINE = line[i]
                if THE_NEXT_LINE == "Bedeutungen":
                    # print("meanings for",record['title'])
                    try:
                        meaning = line[i + 1]
                    except:
                        print("exception in record iteration")
                        return False
    else:
        return False
    return meaning, record['syllables']


class Woerterbuch:
    '''
    Diese Klasse erzeugt (wenn aktiviert)
    eine Liste aus Spielwoerter und ihre Silben und Bedeutungen
    '''
    # replace with escape game file / rewrite using wiktionary_de_parser's method
    def __init__(self, file_path):
        self.file_path = file_path
        self.listofrecords = [] # im Moment leer
        #self.list_of_word_lists = self.get_list_of_word_lists()  # hier 1000 woerter durch die nächste zeile


        # saved a sample in main.py in case the imported parser stops working

    # def get_list_of_word_lists(self):
    #     list_of_word_lists = []
    #     for record in Parser(self.file_path):
    #         if 'langCode' not in record or record['langCode'] != 'de':
    #             continue
    #         result = iterate(record)
    #         if result:
    #             bedeutung, syls = result
    #             if 'ficken' in record["title"] or 'geil' in record["title"]: # diese woerter nicht in der liste nehmen
    #                 continue
    #             simplelistforaword = [record["title"], bedeutung, syls]
    #             list_of_word_lists.append(simplelistforaword) # ein wort zur listen hinfuegen
    #         if len(list_of_word_lists) == 1000: # mit dieser zahl ist die liste voll
    #             return list_of_word_lists
    #
    # def getaword(self):
    #     j = random.randrange(0, 1000)
    #     record = self.listofrecords[j]
    #     if 'langCode' not in record or record['langCode'] != 'de':
    #         return self.getaword()
    #     result = iterate(record)
    #     if result:
    #         bedeutung, syls = result
    #         simplelistforaword = [record["title"], bedeutung, syls]
    #         return simplelistforaword
    #     else:
    #         return self.getaword()

    def quick_get(self, num, list_of_word_lists = None):
        if not list_of_word_lists:
            list_of_word_lists = self.list_of_word_lists
        dictwords = {}
        for i in range(num):
            success = False
            while not success:
                j = random.randrange(0, 1000)
                list = list_of_word_lists[j]
                if "|" in list[1]:
                    continue
                list[1] = list[1][4:]  # remove line number
                list[1] = re.sub('".*?"', '', list[1])  # copied how to remove quoted things
                list[1] = re.sub("''.*?''", '', list[1])
                list[1] = re.sub("<.*?>", '', list[1])
                list[1] = re.sub("[.*?]", '', list[1])
                # list[1] = re.sub("(.*?)", '', list[1]) # never finds such strings?
                # WEITERE WOERTER AUS DEM SPIEL AUSSCHLIESSEN
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
                if len(list[1]) in range(3, 150):
                    success = True
            dictwords[list[0]] = [list[1], list[2]]
        return dictwords
