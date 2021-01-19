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

    def start(self):
        syl_abstand = 0
        counter = 0
        while True:
            counter += 1
            setup.clock.tick(setup.fps)
            player = self.player
            bank = self.bank

            for stuff in event.get():
                if stuff.type == QUIT:
                    quit()

            keys = key.get_pressed()
            player.slide(keys)

            if counter %30 == 0:

            for i in range(len(bank.flat)):
                print("screen ", syl_abstand)
                syl_abstand += 1
                silben = self.rects
                for j in range(len(silben[:i])):
                    alte_silbe = silben[j]
                    alte_silbe.show()
                    alte_silbe.move()
                neue_silbe = silben[i]
                neue_silbe.show()
                neue_silbe.move()
                setup.screen_update(player)

