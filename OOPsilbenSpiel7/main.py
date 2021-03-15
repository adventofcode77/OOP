import pygame as pg
import sys, time, random
from pygame import *
from OOPsilbenSpiel7 import game

class Main:
    file_paths = ['/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml',"/Users/ellie/Downloads/enwiktionary-20210220-pages-articles-multistream.xml"] # backup
    code_de = "de1 de2" #random.choice([f"Der Turm hat vier Ebenen","Gehe zum Feld 6 bei 6 auf dem Schachbrett","Achte auf den Zeichen an der Decke","Der Schlüssel steht unter Angriff","Eine figur wird mit dem Schlüssel rausfliegen","Du brauchst mehr als sechs Schritte","5 links, 3 gerade aus, 2 rechts"])
    code_en = "en1 en2" #random.choice(["The tower has four levels","Go to square 6 by 6 on the chessboard","Pay attention to the signs on the ceiling","The key will be under attack","A figure will flee with the key","You will need more than six steps","Five to the left, 3 forward, 2 to the right"])
    codes = [code_de,code_en]
    score = 0
    def __init__(self):
        self.newgame(Main.codes, Main.score, Main.file_paths)

    def newgame(self,input_codes,score, file_paths):
        pg.init()
        game1 = game.Game(input_codes, file_paths)
        score += round(game1.score, 2)
        code = game1.output_code
        print(f'score: {score},code: {code}')

if __name__ == '__main__':
     Main()
