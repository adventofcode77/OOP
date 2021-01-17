import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel2 import setup

class Silbe:
    def __init__(self,silbe):
        x = random.randint(0,500)
        print(x)
        self.rect = pg.Rect(x,0,20,20)
        self.txt = setup.font.render(silbe,False,setup.black)

    def moverect(self):
        y = self.rect.y
        self.rect.y = y+10

    def show(self):
        setup.screen.blit(self.txt,self.rect)
