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
        self.dictwithkeyname = setup.get_bank()
        self.listofsyls = []
        self.flat = []
        self.font = pg.font.SysFont("Arial",30)


    def get_rects(self):
        rects = []
        for entry in self.dictwithkeyname:
            sylslist = self.dictwithkeyname[entry][1]
            for silbe2 in sylslist:
                x = random.randrange(50,450,50)
                syl = silbe.Silbe(silbe2)
                rects.append(syl)
        print("get rects ",[a.inhalt for a in rects])
        return rects

    def compose(self):
        setup.screen.fill(setup.lila)
        display.update()



