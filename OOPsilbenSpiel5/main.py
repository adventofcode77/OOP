import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel5 import spieler
from OOPsilbenSpiel5 import setup
from OOPsilbenSpiel5 import bank
from OOPsilbenSpiel5 import silbe
from OOPsilbenSpiel5 import game



def main():
    setup.initiate()
    game1 = game.Game()
    game1.bank.runterfallen()


main()


# if __name__ == '__main__':
#     main()
