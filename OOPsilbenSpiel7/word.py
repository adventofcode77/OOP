import pygame as pg
from pygame import *
from OOPsilbenSpiel7 import silbe
import globale_variablen
import math

class Word(globale_variablen.Settings):
    def __init__(self, key, meaning,txtsilben):
        super().__init__()
        self.meaning = meaning.split(" ")
        self.meaning = list(filter(None,self.meaning))
        self.name = key
        self.txtsilben = txtsilben
        self.bits = self.get_bits()
        self.syls = self.make_silben() #[silbe.Silbe("it","word","def inition")] #[silbe.Silbe(a, self.name) for a in silben]
        self.image = self.font.render(self.name, False, self.black)
        self.rect = self.image.get_rect() # draw_rect()?
        self.rect.x = 0 #random.randrange(0,500-self.rect.w,50)


    def get_bits(self):
        definition = self.meaning
        list_of_lists = []
        num_syls = len(self.txtsilben)
        advancement = math.ceil(len(definition)/num_syls)
        if advancement == 0:
            advancement = 1
        while definition:
            list_of_lists.append(definition[:advancement])
            definition = definition[advancement:]
        return list_of_lists # DO NOT FORGET RETURN


    def make_silben(self):
        syls = []
        if len(self.txtsilben)>len(self.bits):
            smaller = len(self.bits)
            bigger = len(self.txtsilben)
        else:
            smaller = len(self.txtsilben)
            bigger = len(self.txtsilben)
        for i in range(smaller):
            bit = self.bits[i]
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it,word,bit)
            syls.append(silbe1)
        for i in range(smaller,bigger):
            bit = "."
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it, word, bit)
            syls.append(silbe1)
        return syls
