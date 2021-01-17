import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel6 import silbe
from OOPsilbenSpiel6 import setup
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

    def runterfallen(self): #recursive?
        print("fall works 4")
        rects = self.get_rects()
        setup.screen.fill(setup.white)
        print("start moving")
        for i in range(10):

            for event in pg.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_n:
                                bool = False


            for j in range(len(rects[:i])):
                rects[j].show()
                rects[j].move()
                pg.display.update()
                print("j ",rects[j].inhalt,rects[j].rect.x,rects[j].rect.y)

            rects[i].show()
            rects[i].move()
            pg.display.update() # zeigt die ganze runde
            print("i ",rects[i].inhalt,rects[i].rect.x,rects[i].rect.y)
            time.sleep(1)
            setup.screen.fill(setup.white) # bereit fuer die naechste runde



