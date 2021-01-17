import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel4 import silbe
from OOPsilbenSpiel4 import setup
import numpy

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        #print(len(self.array))
        self.dict = {} #it was saving the same syllables multiple times

    def add(self,silbe):
        self.array.append(silbe)
        return self.array

    def runterfallen(self):
        print("fall works 4")
        flat_list = list(numpy.concatenate(self.array).flat)
        print(flat_list)
        for item in flat_list:
            self.dict[item] = [0,0]

        #bool = True #while loop ran too long for bool
        while True:
            setup.clock.tick(setup.fps)
            for i in range (1,len(flat_list)-1): # alles neu erstellen

                for event in pg.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_n:
                                exit()


                for each in flat_list[1:i+1]: # lo - lo
                    temp = silbe.Silbe(each,self.dict[each][0],self.dict[each][1])
                    temp.show() # lo 0,0
                    self.dict[each] = [temp.rect.x,temp.rect.y+40] # lo 0,40

                time.sleep(4)

                item = flat_list[i-1] # hal
                temp2 = silbe.Silbe(item,self.dict[item][0],self.dict[item][1])
                temp2.show() # hal 0,0
                self.dict[item] = [temp2.rect.x,temp2.rect.y+40]
                time.sleep(4)
                pg.display.update()

