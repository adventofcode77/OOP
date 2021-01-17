import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel4 import spieler
from OOPsilbenSpiel4 import setup
from OOPsilbenSpiel4 import bank
from OOPsilbenSpiel4 import silbe

class Game:

    def __init__(self):
        pg.init()
        self.user = spieler.Spieler()
        self.bank = bank.Bank()
        print("bank works")
















# if __name__ == '__main__':
#     pass

