import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel4 import setup

class Silbe:
    def __init__(self,silbe,x,y):
        if x == 0:
            x = random.randrange(50,450,50)
        print(silbe,x,y)
        self.rect = pg.Rect(x,y,20,20)
        self.txt = setup.font.render(silbe,False,setup.black)


    def show(self):
        setup.screen.blit(self.txt,self.rect)

    def move(self):
        self.rect.y += 40

