import pygame as pg
import sys, time, random
from pygame import *
from OOPsilbenSpiel7 import game

class Main:
    file_paths = ['/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml',"/Users/ellie/Downloads/enwiktionary-20210220-pages-articles-multistream.xml"] # backup
    code_de = ["La"] # ["Eine Dame, deren Herz schlägt für den Bauern"] #random.choice([f"Der Turm hat vier Ebenen","Gehe zum Feld 6 bei 6 auf dem Schachbrett","Achte auf den Zeichen an der Decke","Der Schlüssel steht unter Angriff","Eine figur wird mit dem Schlüssel rausfliegen","Du brauchst mehr als sechs Schritte","5 links, 3 gerade aus, 2 rechts"])
    binary_code = ["1"] # "01001001"
    def __init__(self):
        self.newgame(Main.code_de, Main.file_paths, Main.binary_code)

    def newgame(self,input_codes,file_paths, binary_code):
        pg.init()
        #print(pg.font.get_fonts())
        game1 = game.Game(input_codes, file_paths, binary_code)
        code = game1.output_code
        print(f'code: {code}')

if __name__ == '__main__':
     Main()
