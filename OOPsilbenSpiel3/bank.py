import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel4 import silbe
from OOPsilbenSpiel4 import setup

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        print(len(self.array))
        self.dict = {}

    def add(self,silbe):
        self.array.append(silbe)
        return self.array

    def runterfallen(self):
        for item in self.array:
             pass #self.dict[item] = [0,0] #can't use list as dict key
        bool = True
        while bool:
            for i in range (1,len(self.array)): # alles neu erstellen
                setup.screen.fill(setup.white)
                for each in self.array[1:i]:
                    temp = silbe.Silbe(each,self.dict[each][0],self.dict[each][1])
                    temp.show()
                    self.dict[each] = [temp.rect.x,temp.rect.y+40]

                for event in pg.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_n:
                                bool = False
                item = self.array[i]
                temp2 = silbe.Silbe(item,self.dict[item][0],self.dict[item][1])
                temp2.move()
                time.sleep(1.5)
                pg.display.update()

