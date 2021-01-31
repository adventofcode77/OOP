import pygame as pg
from pygame import *
from pygame.locals import *
import math

from OOPsilbenSpiel7 import woerter
from OOPsilbenSpiel7 import globale_variablen
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler


class Game(globale_variablen.Settings):

    def __init__(self):
        super().__init__()
        self.player = spieler.Spieler()
        self.bank = woerter.Woerter()
        self.words = self.bank.get_words()
        self.defs = [a.meaning for a in self.words]
        self.txt_syls = self.bank.txtsyls
        self.selected = []
        self.txt = self.font.render("player",False,self.black)
        self.screen = pg.display.set_mode((self.screenh,self.screenw))
        self.score = 0
        self.syls = self.bank.silben
        self.counter = 0
        self.deleted_word_bool = False
        self.deletedlist = []


    def draw_desk(self): # origs
        x,y = self.right,self.down
        mysilben = self.player.my_silben
        print("len mysyls:",len(mysilben))
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(mysilben):
                    syl = mysilben[index]
                    copy = silbe.Silbe(syl.inhalt, syl.word, syl.bit, syl.tuple[0],syl.tuple[1])
                    if syl.clicked_on == True:
                        copy.image = self.font.render(copy.inhalt,False,self.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        # the event loop didn't work inside of this function
        self.screen.fill(self.lila)
        syls = self.draw_desk() # copies
        if click:
            x,y = click
            for syl in syls:
                if syl.rect.collidepoint(x,y):
                    for item in self.player.my_silben: #next()?
                        if item.tuple == syl.tuple:
                            if item.clicked_on:
                                item.clicked_on = False
                                for i in range(len(self.player.appendlist)):
                                    off = self.player.appendlist[i]
                                    if item.tuple == off.tuple:
                                        del self.player.appendlist[i]
                                        break
                                    else:
                                        print(item.inhalt,item.tuple,"for item;",off.inhalt,off.tuple,"for tuple")
                            else:
                                item.clicked_on = True
                                self.draw_word(syl)
        self.draw_word()
        display.flip()


    def draw_word(self,syl=None):
        self.blitword(self.lila) #draws over word and def
        if syl:
            self.player.appendlist.append(syl)
            print(syl.inhalt, "is added to the list")
            if self.deleted_word_bool:
                print("in bool and syl loop")
                self.deleted_word_bool = False
                self.deletedlist = []
        elif self.deleted_word_bool:
            print("in bool loop")
            self.blitword(self.gold)
        else:
            self.blitword(self.black)
        self.check_word()

    def makedefstring(self):
        liste = []
        if self.deleted_word_bool:
            bitlists = [a.bit for a in self.deletedlist]
        else:
            bitlists = [a.bit for a in self.player.appendlist]
        bitstrings = map(" ".join, bitlists)
        defstring = " ".join(bitstrings)
        return defstring

    def blitword(self,farbe):
        if self.deletedlist:
            liste = self.deletedlist
            print("dellist wasn't empty, len",len(self.deletedlist))
        else:
            liste = self.player.appendlist
        wordstring = "".join([a.inhalt for a in liste])
        print("wordstring is",wordstring)
        defstring = self.makedefstring()
        word_image = self.font.render(wordstring, False, farbe)
        def_image = self.font.render(defstring, False, farbe)
        wordrect = word_image.get_rect()
        defrect = def_image.get_rect()
        def split_def():
            lines = math.ceil(defrect.w/self.screenw)
            return self.get_bits(defstring,lines)
        print(defrect.w)
        print(self.screenw)
        print(defrect.w/self.screenw)
        listoflists = split_def()
        screen_rect = Rect(0, 0, self.screenh, self.screenw)
        for i in range(len(listoflists)):
            list = listoflists[i]
            bitimg = self.font.render(" ".join(list),False,self.black)
            bitrect = bitimg.get_rect()
            bitrect.center = screen_rect.center
            self.screen.blit(bitimg, (bitrect.centerx, bitrect.centery+i*(bitrect.h*2)))
        wordrect.center = screen_rect.center
        self.screen.blit(word_image, (wordrect.centerx,wordrect.centery))

    def check_word(self):
        print("len applist", len(self.player.appendlist))
        appendlisttuples = [a.tuple for a in self.player.appendlist]
        for word in self.words:
            wordtuples = [a.tuple for a in word.syls]
            if appendlisttuples == wordtuples:
                self.delete_word()
                self.words.remove(word)

    def delete_word(self): #same syl is actually different objects in different lists, why?
        self.score += 5
        self.counter -= len(self.player.appendlist) # check if working
        for silbe in self.player.appendlist:
            for syl in self.syls:
                if silbe.tuple == syl.tuple:
                    self.syls.remove(syl)
            for syl in self.player.my_silben:
                if silbe.tuple == syl.tuple:
                    self.player.my_silben.remove(syl)
        print("in del")
        self.deletedlist = self.player.appendlist[:]
        print("just made dellist, len",len(self.deletedlist))
        self.player.appendlist = []
        self.deleted_word_bool = True


    def screen_update_and_move(self,allsyls,current_syl,player): # after every changed object
        self.screen.fill(self.zuff)
        for i in range(current_syl):
            syllable = allsyls[i]
            if syllable.visible == True:
                self.screen.blit(syllable.image,syllable.rect) #draw function?
            syllable.rect.y += syllable.speed
        self.screen.blit(player.image,player.rect)
        pg.display.flip()

    def gameloop(self):
        clock = pg.time.Clock()
        run = True
        print([each.name for each in self.words])
        loops = 0
        click = False
        bool = False
        boolcounter = 0
        while True:
            clock.tick(self.fps) #ONE LOOP
            self.score -= 0.005 #quicker play wins more
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                    if stuff.type == QUIT:
                        self.screen.fill(self.black)
                        image_end = self.font.render("GAME OVER",False,self.white)
                        x,y,image_w,h = image_end.get_rect()
                        self.screen.blit(image_end,(self.screenw//2-image_w//2,self.screenh//2))
                        display.flip()
                        print(len(self.player.my_silben))
                        return self.score
                        quit()
                    elif stuff.type == KEYDOWN:
                        if stuff.key == K_SPACE:
                            run = False
                        elif stuff.key == K_a:
                            for item in self.player.my_silben:
                                item.clicked_on = False
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
                            self.screen.fill(self.black)
                            boolcounter += 1
                            image_newloop = self.bigfont.render("NEW LOOP", False, self.white)
                            x, y, image_w, h = image_newloop.get_rect()
                            self.screen.blit(image_newloop, (self.screenw//2-image_w//2,self.screenh//2))
                            display.update()
                            continue

                    else:
                        action = self.player.act() # PLAYER MOVES ONCE A LOOP
                        if action == 1: #how does this work again? return is false
                            run = False
                        self.player.pick(self.syls)
                        if loops % 15 == 0:
                            if self.counter+1 == len(self.syls):
                                print("counter resets")
                                for syl in self.syls:
                                    syl.rect.y = 0
                                self.counter = 0
                                bool = True
                            self.counter += 1
                            loops = 0
                        loops += 1
                        try:
                            self.screen_update_and_move(self.syls,self.counter,self.player)
                        except: # if len(self.syls) == 0
                            image_win = self.bigfont.render(f'YOU WON! \n YOUR SCORE IS {self.score}', False, self.white)
                            x, y, image_w, h = image_newloop.get_rect()
                            self.screen.blit(image_win, (self.screenw // 2 - image_w // 2, self.screenh // 2))
                            display.flip()
                else:
                    self.desk(click)
                    click = False
