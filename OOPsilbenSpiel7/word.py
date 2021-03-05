import pygame as pg
from pygame import *
from OOPsilbenSpiel7 import silbe
import globale_variablen
import math, random

class Word():
    all_syls = []
    def __init__(self, key, meaning,txtsilben,worder,totalsyls,info):
        super().__init__()
        self.info = info
        self.totalsyls = totalsyls
        self.worder = worder
        self.name = key
        self.meaning = [a for a in meaning.split() if a is not None] # remove the empty strings
        self.txtsilben = txtsilben
        Word.all_syls.append(txtsilben)
        self.bits = self.info.get_bits(self.meaning, len(self.txtsilben))
        self.syls = self.make_silben(self.info.make_rgb())
        self.image = self.info.default_font.render(self.name, False, self.info.black)
        self.rect = self.image.get_rect() # draw_rect()?

    def make_silben(self, rgb):
        order = self.totalsyls # make class attribute?
        syls = []
        if len(self.txtsilben)>len(self.bits): # change to a counter?
            smaller = len(self.bits)
            bigger = len(self.txtsilben)
        else:
            smaller = len(self.bits) # changed
            bigger = len(self.txtsilben)
        for i in range(smaller):
            order += 1
            bit = self.bits[i]
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it,word,bit,order, self.worder, self.info, rgb)
            syls.append(silbe1)
        for i in range(smaller,bigger):
            order += 1
            bit = "..."
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it, word, bit, order,self.worder, self.info, rgb)
            syls.append(silbe1)
        return syls
