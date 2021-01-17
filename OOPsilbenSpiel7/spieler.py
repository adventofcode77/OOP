import pygame as pg
import sys, time, random
from pygame.locals import *
import numpy as np
from OOPsilbenSpiel7 import setup

class Spieler:
    def __init__(self):
        l, r, w, h = 200,200,50,20
        self.rect = pg.Rect(l,r,w,h)
        self.pausiert = True
        self.step = 20
        self.my_silben = []
        self.auswahl = []
        self.txt = setup.font.render("player",False,setup.black)

    def show(self):
        setup.screen.blit(self.txt,self.rect)
        print(self.txt,self.rect.x,self.rect.y)


    def onemove(self,event):
        if event.key == K_n: #exit game
            exit()
        elif event.key == K_UP:
            self.rect.y -= 40
        elif event.key == K_DOWN:
            self.rect.y += 40
        elif event.key == K_LEFT:
            self.rect.x -= 40
        elif event.key == K_RIGHT:
            self.rect.x += 40

    def sammeln(self,silbe):
        self.my_silben.append(silbe)

    def pick(self,silbe):
        self.auswahl.append(silbe)


