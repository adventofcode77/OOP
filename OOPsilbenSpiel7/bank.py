import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import setup
import numpy

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        #print(len(self.array))
        self.dict = {} #fehler: saves values to same key for multiple words
        self.flat = list(numpy.concatenate(self.array).flat)

    def get_rects(self):
        rects = []
        for syl in self.flat:
            x = random.randrange(50,450,50)
            hmm = silbe.Silbe(syl,x,0)
            rects.append(hmm)
        return rects

    def add(self,silbe):
        self.array.append(silbe)
        return self.array

    def runterfallen(self,player): #recursive?
        rects = self.get_rects()
        player.show()
        for i in range(len(self.array)):

            for j in range(len(rects[:i])):

                for event in pg.event.get():
                    if event.type == KEYDOWN:
                        player.onemove(event)

                rects[j].show()
                rects[j].move()
                pg.display.update()
                print("j ",rects[j].inhalt,rects[j].rect.x,rects[j].rect.y)

            rects[i].show()
            rects[i].move()
            print("i ",rects[i].inhalt,rects[i].rect.x,rects[i].rect.y)

            player.show()
            pg.display.update() # zeigt die ganze runde


            time.sleep(1)
            setup.screen.fill(setup.lila) # bereit fuer die naechste runde



