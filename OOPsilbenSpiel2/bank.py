import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel2 import silbe

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = ["bei","spiel","bringen","platz"]

    def add(self,silbe):
        self.array.append(silbe)
        return self.array

    def show(self):
        pass
