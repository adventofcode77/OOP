import pygame as pg
import sys, time, random
from pygame import *
import game

class Main:
    def __init__(self):
        self.newgame(0)

    def newgame(self,score):
        pg.init()
        game1 = game.Game()
        loop = game1.gameloop()
        score += loop
        print("score:",score)
        newgame = input("Game over. New game?")
        if newgame == "y":
            self.newgame(score)
        else:
            exit()

if __name__ == '__main__':
     Main()
