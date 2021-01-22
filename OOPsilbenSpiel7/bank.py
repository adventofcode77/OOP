import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import setup
import numpy

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        self.flat = list(numpy.concatenate(self.array).flat)
        self.font = pg.font.SysFont("Arial",30)


    def get_rects(self):
        rects = []
        for syl in self.flat:
            x = random.randrange(50,450,50)
            syl = silbe.Silbe(syl,x,0)
            rects.append(syl)
        return rects

    def compose(self):
        setup.screen.fill(setup.lila)
        display.update()



