import pygame as pg
import random
from OOPsilbenSpiel7 import woerterbuch
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Woerter():
    def __init__(self,game_instance):
        super().__init__()
        self.info = game_instance
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.get_bank()
        self.words = self.get_words()
        self.silben = self.get_silben()

    def get_bank(self):
        file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'
        parser = woerterbuch.Woerterbuch(file_path)
        return parser.parsed

    def get_words(self):
        words = []
        totalsyls = 0
        worder = 0
        for entry in self.dictwithkeyname:
            worder += 1
            name = entry
            meaning = self.dictwithkeyname[entry][0]
            syls = self.dictwithkeyname[entry][1]
            aword = word.Word(name, meaning, syls, worder, totalsyls, self.info)
            words.append(aword)
            totalsyls += len(syls)
        return words

    def get_silben(self):
        sylobjects = []
        for aword in self.words:
            for asyl in aword.syls:
                sylobjects.append(asyl)
        return random.sample(sylobjects,len(sylobjects)) #sample returns new list


