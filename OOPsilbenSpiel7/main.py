import pygame as pg
import sys, time, random
from pygame import *
import gameloop

class Main:
    def __init__(self):
        self.newgame("This is a sample code",0)

    def newgame(self,input_code,score):
        pg.init()
        game1 = gameloop.Gameloop(input_code)
        score += game1.score
        code = game1.output_code
        print(f'score: {score},code: {code}')

if __name__ == '__main__':
     Main()
