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
        self.selected = []
        self.font = pg.font.SysFont("Arial",30)
        self.txt = self.font.render("player",False,setup.black)

    def draw_desk(self):
        setup.screen.fill(setup.lila)
        x,y = setup.right,setup.down
        syls = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(setup.down,setup.down*4,setup.down):
            for x in range(setup.right,setup.right*5,setup.right):
                if index < len(syls):
                    syl = syls[index]
                    copy = silbe.Silbe(syl.inhalt)
                    copy.rect.x,copy.rect.y = x,y
                    setup.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
        display.update()
        return desk_syls

    def desk(self,syls):
        print("in desk")
        for e in event.get():
            print("eventloop?",e.type)
            if e.type == MOUSEBUTTONDOWN:
                print("mouse")
                click = mouse.get_pos()
                for syl in syls:
                    print("for syl")
                    if syl.rect.collidepoint(click):
                        syl.image.fill(setup.white)
                        self.selected.append(syl.inhalt)
                        self.draw_word()

    def draw_word(self):
        word = ""
        for syl in self.selected:
            word += syl
        print(word)
        word_image = self.font.render(word,False,setup.black)
        ww,wh = self.font.size(word)
        setup.screen.blit(word_image,((setup.right+ww)//2,setup.down*6))
        display.update()




    def gameloop(self):
        run = True
        syls = self.rects
        loops = 0
        counter = 0
        index = 0 # NEWEST SYLLABLE INDEX
        copies = []
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
                            copies = self.draw_desk()
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
                    self.desk(copies)





