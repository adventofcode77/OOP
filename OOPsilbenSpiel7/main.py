import pygame as pg
import sys, time, random
from pygame.locals import *
import spieler
import setup
import bank
import silbe
import game



def main():
    pg.init()
    game1 = game.Game()
    game1.gameloop()



main()


# if __name__ == '__main__':
#     main()
