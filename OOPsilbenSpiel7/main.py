import pygame as pg
import sys, time, random
from pygame import *
from OOPsilbenSpiel7 import game

class Main:
    def __init__(self):
        self.newgame("This is a sample code",0)

    def newgame(self,input_code,score):
        pg.init()
        game1 = game.Game(input_code)
        score += round(game1.score, 2)
        code = game1.output_code
        print(f'score: {score},code: {code}')

if __name__ == '__main__':
     Main()
