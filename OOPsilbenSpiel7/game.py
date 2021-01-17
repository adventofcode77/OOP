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
            setup.things_on_screen = [] #start from empty screen
            player.show() #spieler zeigen
            for j in range(len(rects[:i])):

                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        player.onemove(event)
                        player.show() #spieler bewegungen zeigen
                        self.screen_update()

                rects[j].show()
                self.screen_update() #bisherige silben zeigen
                rects[j].move()
                #print("j ",rects[j].inhalt,rects[j].rect.x,rects[j].rect.y)

            rects[i].show() #neue silbe zeigen
            self.screen_update()
            rects[i].move()
            #print("i ",rects[i].inhalt,rects[i].rect.x,rects[i].rect.y)

            time.sleep(1)



    def screen_update(self): # after every changed object
        setup.screen.fill(setup.lila)
        for thing in setup.things_on_screen:
            setup.screen.blit(thing.txt,(thing.rect.x,thing.rect.y))
        pg.display.update()






















# if __name__ == '__main__':
#     pass

