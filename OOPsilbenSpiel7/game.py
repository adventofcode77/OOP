import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import silbe
import numpy

class Game:

    def __init__(self):
        self.player = spieler.Spieler()
        self.bank = bank.Bank()
        self.rects = self.bank.get_rects()
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render("player",False,setup.black)
        # self.allsyls = [[None,None,None,None,None,None,None,None,None,None,a] for a in self.rects]
        # self.allflat = list(numpy.concatenate(self.allsyls).flat)

    def anotherway(self):
        pass

    def loop1(self):
        syls = self.rects
        loops = 0
        counter = 0
        index = 0 # NEWEST SYLLABLE INDEX
        while True:
            setup.clock.tick(setup.fps) #ONE LOOP
            self.player.slide() # PLAYER MOVES ONCE A LOOP
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                if stuff.type == QUIT:
                    quit()
            setup.screen_update_and_move(syls,counter,self.player)
            if loops % 15 == 0:
                counter += 1 if counter <= len(syls) else 0
                loops = 0
            loops += 1
            pg.display.flip()



