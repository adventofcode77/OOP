import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel6 import spieler
from OOPsilbenSpiel6 import setup
from OOPsilbenSpiel6 import bank
from OOPsilbenSpiel6 import silbe
from OOPsilbenSpiel6 import game



def main():
    setup.initiate()
    game1 = game.Game()
    game1.bank.runterfallen()



main()


# if __name__ == '__main__':
#     main()
