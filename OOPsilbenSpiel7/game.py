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

    def anotherway(self):
        pass

    def loop1(self):
        syls = self.rects
        counter = 0
        while True:
            setup.things_on_screen = []
            counter += 1
            print("counter ",counter)
            setup.clock.tick(setup.fps)
            self.player.slide()

            for stuff in event.get():
                if stuff.type == QUIT:
                    quit()

            for i in range(len(syls)):
                neu = syls[i]
                for alt in syls[:i]:
                    alt.move()
                    # print("this time ",counter)
                neu.add()
                neu.move()

            setup.screen_update(self.player)
            print(len(setup.things_on_screen))



