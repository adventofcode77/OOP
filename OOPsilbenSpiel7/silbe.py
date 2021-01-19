import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import setup

class Silbe:
    def __init__(self,silbe,x,y):
        self.inhalt = silbe
        length = len(silbe)*10
        if x == 0:
            x = random.randrange(length,500-length,50)
        self.rect = pg.Rect(x,y,length,20)
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render(silbe,False,setup.black)
        self.speed = 30


    def add(self):
        setup.things_on_screen.append(self)

    def move(self):
        self.rect.y += self.speed

