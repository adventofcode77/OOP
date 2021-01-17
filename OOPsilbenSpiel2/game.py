import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel2 import spieler
from OOPsilbenSpiel2 import setup
from OOPsilbenSpiel2 import bank
from OOPsilbenSpiel2 import silbe

class Game:


    def __init__(self):
        pg.init()
        self.user = spieler.Spieler()
        self.bank = bank.Bank()

    def update_screen(self):
        setup.screen.fill(setup.white)

    def start(self):
        silbe1 = silbe.Silbe("hi")
        bool = True
        while bool:
            #print("iteration")
            setup.screen.fill(setup.white)
            silbe1.show()
            silbe1.moverect()
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    bool = False
            pg.display.update()
            time.sleep(0.5)







# if __name__ == '__main__':
#     pass

