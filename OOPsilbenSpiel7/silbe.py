import pygame as pg
import random
from OOPsilbenSpiel7 import spieler
import globale_variablen
from itertools import *
import math

class Silbe(): #do with sprites
    silbe_all_syls = []
    def __init__(self,it,word,bit,order,worder, info): #or make it inherit from word
        self.info = info
        self.order = order
        self.inhalt = it
        self.word = word
        self.image = self.make_image(random.choice((0,1,2)))
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,self.info.screenw-self.rect.w,self.info.screenw//10)
        self.clicked_on = False
        self.bit = bit # ['einer', 'Aktiengesellschaft']
        self.visible = True
        self.tuple = (order,worder)
        Silbe.silbe_all_syls.append(self)

    def make_image(self, hue): # make three main hues, each for all in a word
        rgb = [100,100,100]
        rgb[0],rgb[1],rgb[2] = random.randint(0,200),random.randint(0,200),random.randint(0,150)
        rgb[hue] = 255
        return self.info.font.render(self.inhalt, False, tuple(rgb))











