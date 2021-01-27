import pygame as pg
import random
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Silbe(globale_variablen.Settings): #do with sprites
    def __init__(self,it,word,bit): #or make it inherit from word
        super().__init__()
        self.inhalt = it
        self.word = word
        self.image = self.font.render(it, False, self.black)
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3
        self.clicked_on = False
        self.bit = " ".join(bit) #giving it a list of lists sometimes
        self.visible = True

    def move(self,speed=5):
        self.rect.y += self.speed

