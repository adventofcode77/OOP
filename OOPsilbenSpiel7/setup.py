import pygame as pg
import sys, time, random
from pygame.locals import *
import linecache
from wiktionary_de_parser import Parser
import parsewikt3
import parsewikt
import numpy

class Settings:
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.zuff = (200,200,200)
        self.lila = (125,33,200)
        self.clock = pg.time.Clock()
        self.fps = 60
        self.things_on_screen = []
        self.pause = False
        self.screenw, self.screenh = 500,500
        self.right = self.screenw//6
        self.down = self.screenh//12
        self.screen = pg.display.set_mode((self.screenh,self.screenw))
        self.font = pg.font.SysFont("Arial",30)
        self.file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'
        self.parser = parsewikt.Parse()
        self.parsed2 = self.parser.parsed
        print(self.parsed2, "\n\nnext\n\n")

    def screen_update_and_move(self,allsyls,current_syl,player): # after every changed object
        self.screen.fill(self.zuff)
        for i in range(current_syl):
            syllable = allsyls[i]
            if syllable.visible == True:
                self.screen.blit(syllable.image,syllable.rect) #draw function?
            syllable.rect.y += syllable.speed
        self.screen.blit(player.image,player.rect)
        pg.display.flip()

    def get_bank(self):
        bank = self.parsed2
        return bank



