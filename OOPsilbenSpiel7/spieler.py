import pygame as pg
from pygame import *
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
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render("player",False,setup.black)
        self.speed = 8

    def add(self):
        setup.things_on_screen.append(self)

    def slide(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            print("left")
            self.rect.x -= self.speed
        elif keys[K_RIGHT]:
            self.rect.x += self.speed
        elif keys[K_UP]:
            self.rect.y -= self.speed
        elif keys[K_DOWN]:
            self.rect.y += self.speed
        #setup.screen.blit(self.txt,self.rect)
        #print(self.rect)



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


