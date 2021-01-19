import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import game



def main():
    pg.init()
    game1 = game.Game()
    game1.start()



main()


# if __name__ == '__main__':
#     main()
