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

    def anotherway(self):
        pass

    def pause(self):
        setup.screen.fill(setup.lila)
        x,y = 20,25
        for each in self.player.my_silben:
            w = each.rect.w
            if x > setup.screenw-w-20:
                if y+each.rect.h >= setup.screenh-25:
                    break
                y += 50
                x = 20
                setup.screen.blit(each.image,(x,y))
                x += w+30
            else:
                setup.screen.blit(each.image,(x,y))
                x += w+50

        display.update()


    def loop1(self):
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
                        elif stuff.key == K_a:
                            run = True
            else:
                if run == True:
                    action = self.player.act() # PLAYER MOVES ONCE A LOOP
                    if action == "composing screen":
                        run = False
                        self.pause()
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
                    self.pause()





