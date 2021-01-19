import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import setup
import numpy

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        #print(len(self.array))
        self.dict = {} #fehler: saves values to same key for multiple words
        self.flat = list(numpy.concatenate(self.array).flat)

    def get_rects(self):
        rects = []
        for syl in self.flat:
            x = random.randrange(50,450,50)
            syl = silbe.Silbe(syl,x,0)
            rects.append(syl)
        return rects

    def add(self,silbe):
        self.array.append(silbe)
        return self.array





