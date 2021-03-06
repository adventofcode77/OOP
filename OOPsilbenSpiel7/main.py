import pygame as pg
import sys, time, random
from pygame import *
from OOPsilbenSpiel7 import game

class Main:
    file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml' #make a failsafe
    code = "1951 oh"
    score = 0
    def __init__(self):
        self.newgame(Main.code, Main.score)

    def newgame(self,input_code,score):
        pg.init()
        game1 = game.Game(input_code)
        score += round(game1.score, 2)
        code = game1.output_code
        print(f'score: {score},code: {code}')

if __name__ == '__main__':
     Main()
