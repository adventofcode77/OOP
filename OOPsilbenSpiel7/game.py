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
            self.bank.runterfallen(self.player)



















# if __name__ == '__main__':
#     pass

