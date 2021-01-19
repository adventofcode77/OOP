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
        alte_silbe = self.rects[alt]
        alte_silbe.show()
        alte_silbe.move()
        neue_silbe = self.rects[neu]
        neue_silbe.show()
        neue_silbe.move()
        setup.screen_update(self.player)
        return [neu if neu>alt+1 else neu+1,alt+1]

    def loop(self,neu,alt,counter):
        if neu == len(self.rects)-1:
            exit()
        print(counter)
        counter += 1
        setup.clock.tick(setup.fps)

        for stuff in event.get():
            if stuff.type == QUIT:
                quit()
        self.player.slide()
        self.loop(self.move_syls(neu,alt)[0],self.move_syls(neu,alt)[1],counter)
        #self.loop(neu if neu>alt+1 else neu+1,alt+1,counter)


