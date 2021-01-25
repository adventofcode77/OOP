import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
import numpy as np
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank

class Spieler:
    def __init__(self):
        l, r, w, h = 200,200,40,40
        self.rect = pg.Rect(l,r,w,h)
        self.pausiert = True
        self.step = 20
        self.my_silben = []
        self.mysyllen = 0
        self.auswahl = []
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render("player",False,setup.black)
        self.image = transform.scale(image.load('Lacrosse_Player.svg'),(self.rect.w,self.rect.h))
        self.speed = 8
        self.word = ""
        self.selected = []

    def add(self):
        setup.things_on_screen.append(self)

    def act(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0+self.speed:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x <= 500-self.speed-self.rect.w:
            self.rect.x += self.speed
        elif keys[K_UP] and self.rect.y >= 0+self.speed:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y <= 500-self.speed-self.rect.w:
            self.rect.y += self.speed
        elif keys[K_SPACE]:
            return False
        elif keys[K_2]:
            self.my_silben = []
            self.word = ""
            self.selected = []
            print("cleared desk")

    def pick(self,sylobjects):
        #print(sylobjects)
        if len(self.my_silben) == 12:
            pass #print("you can only pick 12 at a time!")
        else:
            index = self.rect.collidelist([a.rect for a in sylobjects])
            if index is not -1:
                picked = sylobjects[index]
                if picked not in self.my_silben:
                    self.my_silben.append(picked)


    def use(self,silbe):
        self.auswahl.append(silbe)

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


