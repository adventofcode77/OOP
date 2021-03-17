import pygame as pg
import random
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import globale_variablen
from itertools import *
import math

class Silbe(): #do with sprites
    silbe_all_syls = []
    def __init__(self,it,word,bit,order,worder, info, rgb): #or make it inherit from word
        self.info = info
        self.order = order
        self.inhalt = it
        self.word = word
        self.rgb = rgb
        self.color = rgb
        self.rect = self.info.silbenfont.get_rect(it) # or text.get_rect()?
        self.rect.x = random.randrange(0,self.info.screenw-self.rect.w,self.info.screenw//10)
        self.clicked_on = False
        self.bit = bit # ['einer', 'Aktiengesellschaft']
        self.visible = True
        self.tuple = (order,worder)
        Silbe.silbe_all_syls.append(self)













