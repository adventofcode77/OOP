import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import setup

class Silbe: #do with sprites
    def __init__(self,silbe,x,y):
        self.inhalt = silbe
        font = pg.font.SysFont("Arial",20)
        self.image = font.render(silbe,False,setup.black)
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3
        self.on = False


    def add(self):
        setup.things_on_screen.append(self)

    def move(self,speed=5):
        self.rect.y += self.speed

