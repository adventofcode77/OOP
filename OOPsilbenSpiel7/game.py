import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import silbe

class Game:

    def __init__(self):
        self.player = spieler.Spieler()
        self.bank = bank.Bank()
        self.rects = self.bank.get_rects()
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render("player",False,setup.black)

    def anotherway(self):
        pass

    def loop1(self):
        syls = self.rects
        counter = 0
        index = 0 # NEWEST SYLLABLE INDEX
        while True:
            setup.screen.blit(self.txt,self.player.rect)
            setup.clock.tick(setup.fps) #ONE LOOP
            self.player.slide() # PLAYER MOVES ONCE A LOOP
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                if stuff.type == QUIT:
                    quit()
            setup.screen_update_and_move(syls,counter,self.player)
            counter += 1
            print(len(setup.things_on_screen))
            time.sleep(0.3)



