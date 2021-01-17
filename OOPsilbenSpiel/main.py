import pygame, sys, time, random, tkinter
from pygame.locals import *
from OOPsilbenSpiel import game
from OOPsilbenSpiel import spieler


#pygame.init() #crashes program with tkinter


def main():
    gameobj = game.Game()
    gameobj.show_bank()
    counter = 0
    exit = False
    while not exit:
        print(counter)
        counter += 1

main()

# if __name__ == '__main__':
#     main()
