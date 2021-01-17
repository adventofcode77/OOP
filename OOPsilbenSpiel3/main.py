import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel4 import spieler
from OOPsilbenSpiel4 import setup
from OOPsilbenSpiel4 import bank
from OOPsilbenSpiel4 import silbe
from OOPsilbenSpiel4 import game



def main():
    print("def main works")
    game1 = game.Game()
    game1.bank.runterfallen()

print("main works")
main()


# if __name__ == '__main__':
#     main()
