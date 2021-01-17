import pygame as pg
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel5 import silbe
from OOPsilbenSpiel5 import setup
import numpy

class Bank:
    def __init__(self):
        self.rect = pg.Rect(0,0,20,20)
        self.array = setup.get_bank()
        #print(len(self.array))
        self.dict = {} #fehler: saves values to same key for multiple words

    def add(self,silbe):
        self.array.append(silbe)
        return self.array

    def runterfallen(self): #recursive?
        print("fall works 4")
        flat_list = list(numpy.concatenate(self.array).flat)
        print(flat_list)
        for item in flat_list:
            self.dict[item] = [[0, 0, 0]]

        #bool = True #while loop ran too long for bool
        while True:
            setup.clock.tick(setup.fps)
            setup.screen.fill(setup.col)
            pg.display.update()
            for i in range (1,len(flat_list)-1): # alles neu erstellen
                setup.screen.fill(setup.col)
                for event in pg.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_n:
                                exit()


                for j in range (0, len(flat_list[:i])):
                    each = flat_list[j]
                    valueslist = self.dict[each]
                    print("vallist ",each,valueslist)
                    check1 = 0
                    for value in valueslist:
                        temp = silbe.Silbe(each,value[0],value[1])
                        temp.show()
                        if value[2] == j:
                            check1 = 1
                            value = [temp.rect.x,temp.rect.y+40,j]
                    if check1 == 0:
                        pass #nothing works, have to rewrite
                            #self.dict[each].append([temp.rect.x,temp.rect.y+40,j])
                            # temp = silbe.Silbe(each,value[0],value[1])
                            # temp.show()
                            #     print("pre ",value, self.dict[each])
                            #     value = [[temp.rect.x,temp.rect.y+40,j]]
                            #     print("post ",value,self.dict[each])

                time.sleep(0.5)

                item = flat_list[i] # hal
                valueslist = self.dict[item]
                check2 = 5
                for value in valueslist:
                    temp2 = silbe.Silbe(item,value[0],value[1])
                    temp2.show() # hal 0,0
                    if value == [0,0,0]:
                        value = [[temp2.rect.x,temp2.rect.y+40,i]]
                    elif value[2] == i:
                        check2 = 10
                        value = [[temp2.rect.x,temp2.rect.y+40,i]]
                print("all shown")
                if check2 == 5:
                    self.dict[item].append([temp2.rect.x,temp2.rect.y+40,i])
                time.sleep(0.5)
                pg.display.update()


