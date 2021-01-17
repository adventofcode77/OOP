import pygame as pg
import sys, time, random
from pygame.locals import *
import numpy as np

class Spieler:
    def __init__(self):
        l, r, w, h = 20,20,20,20
        self.avatar = pg.Rect(l,r,w,h)
        self.pausiert = True
        self.step = 20
        self.links, self.oben = -1,-1
        self.rechts, self.unten = 1,1
        self.my_silben = []
        self.auswahl = []

    def go(self,richtung):
        self.rect.richtung += richtung * self.step

    def sammeln(self,silbe):
        self.my_silben.append(silbe)

    def pick(self,silbe):
        self.auswahl.append(silbe)


