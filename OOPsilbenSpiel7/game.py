import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import word
import numpy

class Game:

    def __init__(self):
        #self.player.base = setup.Settings()
        self.player = spieler.Spieler()
        self.bank = bank.Bank()
        self.words = self.bank.get_words()
        self.txt_syls = self.bank.txtsyls
        self.selected = []
        self.font = pg.font.SysFont("Arial",20)
        self.bigfont = pg.font.SysFont("Arial",30)
        self.txt = self.font.render("player",False,self.player.base.black)
        self.sprites = sprite.Group()

    def draw_desk(self): # origs
        x,y = self.player.base.right,self.player.base.down
        sylobjects = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.player.base.down,self.player.base.down*4,self.player.base.down):
            for x in range(self.player.base.right,self.player.base.right*5,self.player.base.right):
                if index < len(sylobjects):
                    syl = sylobjects[index]
                    copy = silbe.Silbe(syl.inhalt,syl.word,syl.bit)
                    if syl.on == True:
                        #print("syl on")
                        copy.image = self.font.render(copy.inhalt,False,self.player.base.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.player.base.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        # the event loop didn't work inside of this function
        self.player.base.screen.fill(self.player.base.lila)
        syls = self.draw_desk() # copies
        if click:
            x,y = click
            for syl in syls:
                if syl.rect.collidepoint(x,y):
                    for item in self.player.my_silben: #next()?
                        if item.inhalt == syl.inhalt:
                            item.on = True
                            #print(item.inhalt," on")
                    self.player.selected.append(syl)
        self.draw_word()
        self.check_word()
        display.update()


    def draw_word(self):
        word = ""
        definition = ""
        for syl in self.player.selected:
            word += f' {syl.inhalt}'
            definition += syl.bit
        #print(word)
        word_image = self.font.render(word,False,self.player.base.black)
        def_image = self.font.render(definition,False,self.player.base.black)
        ww,wh = self.font.size(word)
        dw,dh = self.font.size(definition)
        self.player.base.screen.blit(word_image,((self.player.base.screenw-ww)//2,self.player.base.down*6))
        self.player.base.screen.blit(def_image,((self.player.base.screenw-dw)//2,self.player.base.down*7))
        self.player.word = word

    def check_word(self):
        if self.player.word in self.words:
            if all(a.word == self.player.selected[0].word for a in self.player.selected):
                correct_image = self.font.render("correct",False,self.player.base.white)
                cw,ch = self.font.size("correct")
                self.player.base.screen.blit(correct_image,((self.player.base.screenw-cw)//2,self.player.base.down*7))
                print("correct")



    def gameloop(self):
        self.sprites.add(self.bank.words)
        run = True
        print([each.name for each in self.words])
        sylobjects = self.bank.silben
        loops = 0
        counter = 0
        click = False
        bool = False
        boolcounter = 0
        while True:
            self.player.base.clock.tick(self.player.base.fps) #ONE LOOP
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                    if stuff.type == QUIT:
                        print(len(self.player.my_silben))
                        exit()
                    elif stuff.type == KEYDOWN:
                        if stuff.key == K_SPACE:
                            run = False
                        elif stuff.key == K_a:
                            run = True
                    elif stuff.type == MOUSEBUTTONDOWN:
                        click = mouse.get_pos()
            else:
                if run == True:
                    if bool == True:
                        if boolcounter == 30:
                            bool = False
                            boolcounter = 0
                        else:
                            self.player.base.screen.fill(self.player.base.black)
                            boolcounter += 1
                            self.player.base.screen.blit(self.bigfont.render("new loop",False,self.player.base.white),(200,250))
                            display.update()
                            continue

                    else:
                        action = self.player.act() # PLAYER MOVES ONCE A LOOP
                        if action == 1: #how does this work again? return is false
                            run = False
                        picked = self.player.pick(sylobjects)
                        if loops % 15 == 0:
                            if counter+1 == len(sylobjects):
                                print("counter resets")
                                for syl in sylobjects:
                                    syl.rect.y = 0
                                counter = 0
                                bool = True
                            counter += 1
                            loops = 0
                        loops += 1
                        self.player.base.screen_update_and_move(sylobjects,counter,self.player)
                else:
                    self.desk(click)
                    click = False





