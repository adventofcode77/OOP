import pygame as pg
import random
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Silbe(globale_variablen.Settings): #do with sprites
    def __init__(self,it,word,bit): #or make it inherit from word
        #self.spieler.base = setup.Settings()
        self.spieler = spieler.Spieler()
        self.inhalt = it
        self.word = word
        font = pg.font.SysFont("Arial",20)
        self.image = font.render(it, False, self.spieler.black)
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3
        self.on = True
        self.bit = bit #giving it a list of lists sometimes
        self.visible = True

    def move(self,speed=5):
        self.rect.y += self.speed

