import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import silbe
import numpy

class Game:

    def __init__(self):
        self.player = spieler.Spieler()
        self.bank = bank.Bank()
        self.rects = self.bank.get_rects()
        self.font = pg.font.SysFont("Arial",30)
        self.txt = self.font.render("player",False,setup.black)

    def draw_desk(self):
        setup.screen.fill(setup.lila)
        right = setup.screenw//6
        down = setup.screenh//12
        x,y = right,down
        syls = self.player.my_silben
        index = 0
        # for syl in self.player.my_silben:
        #     setup.screen.blit(syl.image,(x,y))
        #     x += syl.rect.w+right
        #     if x > setup.screenw - right:
        #         y += down
        #         x = right

        for y in range(down,down*4,down):
            for x in range(right,right*5,right):
                if index < len(syls):
                    print(index,len(syls))
                    print(syls[index].inhalt)
                    syl = syls[index]
                    setup.screen.blit(syl.image,(x,y))
                    print("got here")
                    index += 1
        display.update()

    def desk(self):
        self.draw_desk()


    def gameloop(self):
        run = True
        syls = self.rects
        loops = 0
        counter = 0
        index = 0 # NEWEST SYLLABLE INDEX
        while True:
            setup.clock.tick(setup.fps) #ONE LOOP
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                    if stuff.type == QUIT:
                        print([each.inhalt for each in self.player.my_silben])
                        print(len(self.player.my_silben))
                        exit()
                    elif stuff.type == KEYDOWN:
                        if stuff.key == K_SPACE:
                            run = False
                            self.draw_desk()
                        elif stuff.key == K_a:
                            run = True
            else:
                if run == True:
                    action = self.player.act() # PLAYER MOVES ONCE A LOOP
                    if action == 1:
                        run = False
                    self.player.pick(syls)
                    if loops % 15 == 0:
                        if counter + 1 == len(syls):
                            counter = 0
                        else:
                            counter += 1
                        loops = 0
                    setup.screen_update_and_move(syls,counter,self.player)
                    loops += 1
                    pg.display.flip()
                else:
                    self.desk()





