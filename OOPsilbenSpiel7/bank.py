import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import spieler

class Bank:
    def __init__(self):
        self.spieler = spieler.Spieler()
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.spieler.base.get_bank()
        self.txtsyls = self.randomize_syls()
        self.flat = []
        self.font = pg.font.SysFont("Arial",30)
        self.words = self.get_words()
        self.silben = self.get_silben()
        self.test = 3


    def get_words(self):
        words = []
        for entry in self.dictwithkeyname:
            name = entry
            meaning = self.dictwithkeyname[entry][0]
            syls = self.dictwithkeyname[entry][1]
            aword = word.Word(name,meaning,syls)
            words.append(aword)
        #print("get  ",[a.name for a in words])
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


