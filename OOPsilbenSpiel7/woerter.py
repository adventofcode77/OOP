import pygame as pg
import random
from OOPsilbenSpiel7 import woerterbuch
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Woerter(globale_variablen.Settings):
    def __init__(self):
        super().__init__()
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.get_bank()
        self.txtsyls = self.randomize_syls()
        self.flat = []
        self.font = pg.font.SysFont("Arial",30)
        self.test = 0
        self.words = self.get_words()
        self.silben = self.get_silben()


    def get_words(self):
        words = []
        c = 0
        for entry in self.dictwithkeyname:
            self.test += 1
            name = entry
            meaning = self.dictwithkeyname[entry][0]
            syls = self.dictwithkeyname[entry][1]
            aword = word.Word(name,meaning,syls)
            words.append(aword)
        return words

    def get_silben(self):
        sylobjects = []
        for aword in self.words:
            for asyl in aword.syls:
                sylobjects.append(asyl)
        return sylobjects

    def randomize_syls(self):
        all_syls = []
        ditems = self.dictwithkeyname.items()
        for key, value in ditems:
            meaning, syls = value[0], value[1]
            for syl in syls:
                all_syls += [syl]
        return random.sample(all_syls, len(all_syls)) #sample returns new list


    def get_bank(self):
        file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'
        parser = woerterbuch.Woerterbuch(file_path)
        bank = parser.parsed
        return bank
