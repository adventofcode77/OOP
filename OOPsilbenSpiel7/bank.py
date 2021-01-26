import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import silbe, parsewikt
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import spieler

class Bank:
    def __init__(self):
        self.spieler = spieler.Spieler()
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.get_bank2()
        self.txtsyls = self.randomize_syls()
        self.flat = []
        self.font = pg.font.SysFont("Arial",30)
        print("works before init words")
        self.test = 3
        self.words = self.get_words()
        print("just in case")
        self.silben = self.get_silben()
        print("init bank")


    def get_words(self):
        words = []
        c = 0
        for entry in self.dictwithkeyname:
            self.test += 1
            name = entry
            meaning = self.dictwithkeyname[entry][0]
            syls = self.dictwithkeyname[entry][1]
            aword = word.Word(name,meaning,syls)
            print("inside get words before append")
            words.append(aword)
            print(self.test, name)
        #print("get  ",[a.name for a in words])
        print("inside get words return")
        return words

    def get_silben(self):
        sylobjects = []
        for aword in self.words:
            #print(aword.syls)
            for asyl in aword.syls:
                sylobjects.append(asyl)
        #print([a.inhalt for a in sylobjects])
        return sylobjects

    def randomize_syls(self):
        all_syls = []
        ditems = self.dictwithkeyname.items()
        for key, value in ditems:
            meaning, syls = value[0], value[1]
            for syl in syls:
                all_syls += [syl]
        #print(random.sample(all_syls, len(all_syls)))
        return random.sample(all_syls, len(all_syls)) #sample returns new list
        #return all_syls


    def get_bank2(self):
        file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'
        parser = parsewikt.Parse(file_path)
        bank2 = parser.parsed
        print(bank2, "\n\nnext\n\n")
        return bank2
