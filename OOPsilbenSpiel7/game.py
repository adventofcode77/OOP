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
        self.player = spieler.Spieler()
        self.bank = bank.Bank()
        self.words = self.bank.get_words()
        self.txt_syls = self.bank.txtsyls
        self.selected = []
        self.font = pg.font.SysFont("Arial",20)
        self.bigfont = pg.font.SysFont("Arial",30)
        self.txt = self.font.render("player",False,setup.black)
        self.sprites = sprite.Group()

    def draw_desk(self): # origs
        x,y = setup.right,setup.down
        sylobjects = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(setup.down,setup.down*4,setup.down):
            for x in range(setup.right,setup.right*5,setup.right):
                if index < len(sylobjects):
                    syl = sylobjects[index]
                    copy = silbe.Silbe(syl.inhalt,syl.word,syl.bit)
                    if syl.on == True:
                        #print("syl on")
                        copy.image = self.font.render(copy.inhalt,False,setup.white)
                    copy.rect.x,copy.rect.y = x,y
                    setup.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        # the event loop didn't work inside of this function
        setup.screen.fill(setup.lila)
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
            word += " " + syl.inhalt
            definition += syl.bit
        #print(word)
        word_image = self.font.render(word,False,setup.black)
        def_image = self.font.render(definition,False,setup.black)
        ww,wh = self.font.size(word)
        dw,dh = self.font.size(definition)
        setup.screen.blit(word_image,((setup.screenw-ww)//2,setup.down*6))
        setup.screen.blit(def_image,((setup.screenw-dw)//2,setup.down*7))
        self.player.word = word

    def check_word(self):
        if self.player.word in self.words:
            if all(a.word == self.player.selected[0].word for a in self.player.selected):
                correct_image = self.font.render("correct",False,setup.white)
                cw,ch = self.font.size("correct")
                setup.screen.blit(correct_image,((setup.screenw-cw)//2,setup.down*7))
                print("correct")



    def gameloop(self):
        self.sprites.add(self.bank.words)
        run = True
        words = self.words
        sylobjects = self.bank.silben
        loops = 0
        counter = 0
        index = 0 # NEWEST SYLLABLE INDEX
        copies = []
        click = False
        bool = False
        boolcounter = 0
        while True:
            setup.clock.tick(setup.fps) #ONE LOOP
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                    if stuff.type == QUIT:
                        print([each.name for each in self.words])
                        print(len(self.player.my_silben))
                        exit()
                    elif stuff.type == KEYDOWN:
                        if stuff.key == K_SPACE:
                            run = False
                            setup.screen.fill(setup.lila)
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
                            setup.screen.fill(setup.black)
                            boolcounter += 1
                            print("boolcounter:",boolcounter)
                            setup.screen.blit(self.bigfont.render("new loop",False,setup.white),(200,250))
                            display.update()
                            continue

                    else:

                        #print("allsyls len:",len(self.bank.silben))
                        action = self.player.act() # PLAYER MOVES ONCE A LOOP
                        if action == 1: #how does this work again? return is false
                            run = False
                        elif action == 5:
                            for syl in self.player.syls_for_game:
                                syl.visible = True
                            #sylobjects = self.player.syls_for_game + sylobjects
                            #counter += len(self.player.syls_for_game)
                        picked = self.player.pick(sylobjects)
                        if loops % 15 == 0:
                            if counter + 1 == len(sylobjects):
                                print("counter resets")
                                for syl in sylobjects:
                                    syl.rect.y = 0 # doesn't work for small word banks
                                counter = 0
                                display.update()
                                bool = True
                            #
                            # else:
                            counter += 1
                            loops = 0
                        setup.screen_update_and_move(sylobjects,counter,self.player)
                        loops += 1
                        pg.display.flip()
                else:
                    self.desk(click)
                    click = False





