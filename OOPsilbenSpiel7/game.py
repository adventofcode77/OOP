import pygame as pg
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
        print("game works")

    def start(self):
        while True:
            self.runterfallen()

    def runterfallen(self): #recursive?
        player = self.player
        bank = self.bank
        rects = bank.get_rects()
        for i in range(len(bank.flat)):
            setup.things_on_screen = [player] #start from empty screen
            for j in range(len(rects[:i])):

                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        player.onemove(event)
                        player.show() #spieler bewegungen zeigen

                rects[j].show()
                rects[j].move()

            rects[i].show() #neue silbe zeigen
            rects[i].move()

            time.sleep(1)


























# if __name__ == '__main__':
#     pass

