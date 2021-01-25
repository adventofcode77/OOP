import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import setup

class Silbe: #do with sprites
    def __init__(self,it,word,bit):
        self.inhalt = it
        self.word = word
        font = pg.font.SysFont("Arial",20)
        self.image = font.render(it,False,setup.black)
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3
        self.on = False
        self.bit = bit #giving it a list of lists sometimes

    def move(self,speed=5):
        self.rect.y += self.speed

