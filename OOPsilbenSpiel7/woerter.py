import pygame as pg
import random
from OOPsilbenSpiel7 import woerterbuch
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Woerter():
    all_syls = []
    def __init__(self,game_instance, input_code):
        self.info = game_instance
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.get_bank()
        self.words = self.get_words()
        self.silben = self.get_silben()
        self.code_syls = []
        self.split_string_into_syls(input_code)

    def get_bank(self):
        parser = woerterbuch.Woerterbuch()
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
            Woerter.all_syls.append([syl for syl in syls])
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

    # def split_string_into_syls(self, string):
    #     string.split()
    #     all_syls = []
    #     for word in string:
    #         all_syls.append(self.split_word_syls(word))












