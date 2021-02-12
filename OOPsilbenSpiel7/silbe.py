import pygame as pg
import random
from OOPsilbenSpiel7 import spieler
import globale_variablen
from itertools import *
import math

class Silbe(globale_variablen.Settings): #do with sprites
    silbe_all_syls = []
    def __init__(self,it,word,bit,order,worder): #or make it inherit from word
        super().__init__()
        self.order = order
        self.inhalt = it
        self.word = word
        self.image = self.make_image()
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3
        self.clicked_on = False
        self.bit = bit # ['einer', 'Aktiengesellschaft']
        self.visible = True
        self.tuple = (order,worder)
        Silbe.silbe_all_syls.append(self)


    def move(self,speed=5):
        self.rect.y += self.speed

    def make_image(self):
        r = random.randint(100,255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        sylcolor = (r,g,b)
        return self.font.render(self.inhalt, False, sylcolor)











