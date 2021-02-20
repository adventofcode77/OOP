import pygame as pg
from pygame import *
from pygame.locals import *
import random
from OOPsilbenSpiel7 import woerter
from OOPsilbenSpiel7 import globale_variablen
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler


class Game(globale_variablen.Settings,woerter.Woerter,silbe.Silbe,spieler.Spieler):

    def __init__(self):
        super().__init__()
        self.screen_via_display_set_mode = pg.display.set_mode((0, 0), RESIZABLE)
        self.screenw, self.screenh = self.screen_via_display_set_mode.get_rect().size
        self.right = self.screenw // 6
        self.down = self.screenh//12
        self.player = spieler.Spieler(self)
        self.bank = woerter.Woerter(self)
        self.words = self.bank.get_words()
        self.defs = [a.meaning for a in self.words]
        self.selected = []
        print(self.screenw,self.screenh)
        self.screen_copy  = self.screen_via_display_set_mode.copy()
        # followed a post on resizable pygame screen; it doesn't stretch the game, only the empty screen space
        self.score = 0
        self.syls = self.bank.silben
        #self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.counter = 0
        self.deleted_word_bool = False
        self.deletedlist = []
        self.cs = 0
        self.poslist = self.get_pos_list()
        self.screensyls = self.get_screensyls()

    def draw_desk(self): # origs
        mysilben = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(mysilben):
                    syl = mysilben[index]
                    copy = silbe.Silbe(syl.inhalt, syl.word, syl.bit, syl.tuple[0], syl.tuple[1], syl.info)
                    # why didn't syl.copy() work?
                    if syl.clicked_on == True:
                        copy.image = self.font.render(copy.inhalt,False,self.lime)
                    else:
                        copy.image = self.font.render(copy.inhalt, False, self.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.screen_copy.blit(copy.image, copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        # the event loop didn't work inside of this function
        self.screen_copy.fill(self.black)
        syls = self.draw_desk() # copies
        if click:
            x,y = click
            for syl in syls:
                if syl.rect.collidepoint(x,y):
                    for item in self.player.my_silben: #next()?
                        if item.tuple == syl.tuple: # couldn't find syl objects in lists where i'd previously put them
                            if item.clicked_on:
                                item.clicked_on = False
                                for i in range(len(self.player.appendlist)):
                                    off = self.player.appendlist[i]
                                    if item.tuple == off.tuple:
                                        del self.player.appendlist[i]
                                        break
                            else:
                                item.clicked_on = True
                                self.draw_word(syl)
        self.draw_word()
        self.screen_transfer()


    def draw_word(self,syl=None):
        self.blit_word(farbe=(self.lila, self.lila)) #draws over word and def
        if syl:
            self.player.appendlist.append(syl)
            if self.deleted_word_bool:
                self.deleted_word_bool = False
                self.deletedlist = []
        self.blit_word()
        self.check_word()

    def make_def_string(self):
        if self.deleted_word_bool:
            bitlists = [a.bit for a in self.deletedlist]
        else:
            bitlists = [a.bit for a in self.player.appendlist]
        bitstrings = map(" ".join, bitlists)
        defstring = " ".join(bitstrings)
        return defstring

    def blit_word(self, farbe=None):
        # replace with a pygame gui that works with sql?
        if farbe is not (self.lila, self.lila):
            farbe = (self.yellow, self.yellow) if self.deleted_word_bool else (self.lime, self.cyan)
        liste = self.player.appendlist
        wordstring = "".join([a.inhalt for a in liste])
        defstring = self.make_def_string()
        word_image = self.font.render(wordstring, False, farbe[0])
        def_image = self.deffont.render(defstring, False, self.black)
        wordrect = word_image.get_rect()
        defrect = def_image.get_rect()
        def split_def():
            lines = defrect.w / (self.screenw // 2)  # why does half of screen work instead of whole?
            return self.get_bits(defstring, lines)
        listoflists = split_def()
        screen_rect = pg.Rect(0, 0, self.screenw, self.screenh)
        #print(f'center of screen_rect from which to blit word def is {screen_rect.x,screen_rect.y}'
        #      f'current screen size is {self.screenw,self.screenh}')
        for i in range(len(listoflists)):
            list = listoflists[i]
            bitimg = self.deffont.render(" ".join(list), False, farbe[1])
            bitrect = bitimg.get_rect()
            bitrect.center = screen_rect.center
            self.screen_copy.blit(bitimg, (bitrect.x, bitrect.y + (i + 1) * bitrect.h))
        wordrect.center = screen_rect.center
        self.screen_copy.blit(word_image, (wordrect.x, wordrect.y))

    def check_word(self):
        appendlisttuples = [a.tuple for a in self.player.appendlist]
        for word in self.words:
            wordtuples = [a.tuple for a in word.syls]
            if appendlisttuples == wordtuples:
                self.delete_word()
                self.words.remove(word)

    def delete_word(self): #same syl is actually different objects in different lists, why?
        self.score += 5
        for this in self.player.appendlist:
            for syl in self.syls:
                if this.tuple == syl.tuple:
                    index = self.syls.index(syl)
                    if len(self.syls) <len(self.poslist):
                        replacement = silbe.Silbe("o", "word", ["bit"], 404, 404, self)
                        replacement.visible = False
                        self.syls[index] = replacement
                    else:
                        self.syls.remove(syl)
                    self.sylscounter -= 1
            for syl in self.player.my_silben:
                if this.tuple == syl.tuple:
                    self.player.my_silben.remove(syl)
        self.deletedlist = self.player.appendlist[:]
        self.player.appendlist = []
        self.deleted_word_bool = True

    def get_pos_list(self):
        poslist = []
        tenth = self.screenh // 10
        pos = self.screenh - tenth
        while pos >=0-self.counter:
            poslist.append(pos)
            pos -= tenth
        return poslist

    def get_screensyls(self):
        syls = self.syls[self.cs:] + self.syls[:self.cs]
        return syls[:len(self.poslist)] # (now syls should always be bigger than this cut)

    def blit_loop(self): # why is there some trembling?
        self.screensyls = self.get_screensyls()
        self.screen_copy.fill(self.black)
        for i in range(len(self.poslist)):
            if self.screensyls:
                syl = self.screensyls.pop(0)
                if syl.visible == True:
                    self.screen_copy.blit(syl.image, (syl.rect.x, self.poslist[i] + self.counter))
                else:
                    self.screen_copy.blit(self.invisible, (syl.rect.x, self.poslist[i] + self.counter))
                syl.rect.y = self.poslist[i] + self.counter
        self.counter += 5
        if self.counter >= self.screenh // 10:
            self.counter = 0
            self.cs += 1
            if self.cs > len(self.syls)-1: # "==" doesn't work after words get deleted
                self.cs = 0
        self.screen_copy.blit(self.player.image, self.player.rect)
        self.screen_transfer()

    def screen_transfer(self):
        resized_fake_screen = pg.transform.scale(self.screen_copy, self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_fake_screen, (0, 0))
        pg.display.flip()


