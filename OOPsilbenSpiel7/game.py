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

    def move_syls(self,neu,alt):
        setup.screen_update(self.player)
        neu = alt+1
        alte_silbe = self.rects[alt]
        alte_silbe.show()
        alte_silbe.move()
        if neu == alt:
            neue_silbe = self.rects[neu]
            neue_silbe.show()
            neue_silbe.move()
            return neu+1,0
        else:
            return neu,alt+1
        #return neu+1 if neu==alt+1 else neu,alt+1

    def loop(self,neu,alt,counter):
        if neu == len(self.rects)-1:
            self.loop(0,0,0)
        #print(counter)
        counter += 1
        setup.clock.tick(setup.fps)
        for stuff in event.get():
            if stuff.type == QUIT:
                quit()
        self.player.slide()
        neu, alt = self.move_syls(neu,alt)
        print(neu,alt)
        self.loop(neu,alt,counter)


