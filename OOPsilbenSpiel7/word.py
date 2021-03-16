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
        self.meaning = meaning.split()
        for i in range(len(self.meaning)):
            if not self.meaning[i]:
                self.meaning.insert(i,"...")
        self.txtsilben = txtsilben
        Word.all_syls.append(txtsilben)
        self.bits = self.info.get_bits(self.meaning, len(self.txtsilben))
        self.syls = self.make_silben(self.info.make_rgb())
        self.image = self.info.default_font.render(self.name, False, self.info.gold)
        self.rect = self.image.get_rect() # draw_rect()?

    def make_silben(self, rgb):
        order = self.totalsyls # make class attribute?
        syls = []
        for i in range(len(self.txtsilben)):
            order += 1
            it = self.txtsilben[i]
            if i < len(self.bits):
                bit = self.bits[i]
            else:
                bit = [...]
            word = self.name
            silbe1 = silbe.Silbe(it,word,bit,order, self.worder, self.info, rgb)
            syls.append(silbe1)
            order += 1
        return syls
