import pygame as pg
import sys, time, random
from pygame import *
import gameloop

class Main:
    def __init__(self):
        self.newgame(0)

    def newgame(self,score):
        pg.init()
        game1 = gameloop.Gameloop()
        score += game1.score
        print("score:",score)

if __name__ == '__main__':
     Main()
