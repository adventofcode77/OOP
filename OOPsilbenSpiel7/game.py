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
        self.selected = []
        self.screen = pg.display.set_mode((self.screenh,self.screenw))
        self.score = 0
        self.syls = self.bank.silben
        self.counter = 0
        self.deleted_word_bool = False
        self.deletedlist = []
        self.cs = 0
        self.poslist = self.get_poslist()
        self.screensyls = self.get_screensyls()
        self.generated = silbe.Silbe("o","word",["bit"],404,404)
        self.generated.image = self.font.render("o", False, self.gold)
        self.silbe_all_syls = silbe.Silbe.silbe_all_syls


    def draw_desk(self): # origs
        x,y = self.right,self.down
        mysilben = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(mysilben):
                    syl = mysilben[index]
                    copy = silbe.Silbe(syl.inhalt, syl.word, syl.bit, syl.tuple[0],syl.tuple[1])
                    if syl.clicked_on == True:
                        copy.image = self.font.render(copy.inhalt,False,self.lime)
                    else:
                        copy.image = self.font.render(copy.inhalt, False, self.white)
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
                                item.clicked_on = True
                                self.draw_word(syl)
        self.draw_word()
        display.flip()


    def draw_word(self,syl=None):
        self.blitword(farbe=(self.lila,self.lila)) #draws over word and def
        if syl:
            self.player.appendlist.append(syl)
            if self.deleted_word_bool:
                self.deleted_word_bool = False
                self.deletedlist = []
        self.blitword()
        self.check_word()

    def makedefstring(self):
        if self.deleted_word_bool:
            bitlists = [a.bit for a in self.deletedlist]
        else:
            bitlists = [a.bit for a in self.player.appendlist]
        bitstrings = map(" ".join, bitlists)
        defstring = " ".join(bitstrings)
        return defstring

    def blitword(self, farbe=None):
        if farbe is not (self.lila, self.lila):
            farbe = (self.yellow, self.yellow) if self.deleted_word_bool else (self.lime, self.cyan)
        liste = self.player.appendlist
        wordstring = "".join([a.inhalt for a in liste])
        defstring = self.makedefstring()
        word_image = self.font.render(wordstring, False, farbe[0])
        def_image = self.deffont.render(defstring, False, self.black)
        wordrect = word_image.get_rect()
        defrect = def_image.get_rect()

        def split_def():
            lines = defrect.w / (self.screenw // 2)  # why does half of screen work instead of whole?
            return self.get_bits(defstring, lines)
        listoflists = split_def()
        screen_rect = Rect(0, 0, self.screenh, self.screenw)
        for i in range(len(listoflists)):
            list = listoflists[i]
            bitimg = self.deffont.render(" ".join(list), False, farbe[1])
            bitrect = bitimg.get_rect()
            bitrect.center = screen_rect.center
            self.screen.blit(bitimg, (bitrect.x, bitrect.y + (i + 1) * bitrect.h))
        wordrect.center = screen_rect.center
        self.screen.blit(word_image, (wordrect.x, wordrect.y))

    def check_word(self):
        appendlisttuples = [a.tuple for a in self.player.appendlist]
        for word in self.words:
            wordtuples = [a.tuple for a in word.syls]
            if appendlisttuples == wordtuples:
                self.delete_word()
                self.words.remove(word)

    def delete_word(self): #same syl is actually different objects in different lists, why?
        self.score += 5
        for silbe in self.player.appendlist:
            for syl in self.syls:
                if silbe.tuple == syl.tuple:
                    self.syls.remove(syl)
            for syl in self.player.my_silben:
                if silbe.tuple == syl.tuple:
                    self.player.my_silben.remove(syl)
        self.deletedlist = self.player.appendlist[:]
        self.player.appendlist = []
        self.deleted_word_bool = True

    def get_poslist(self):
        poslist = []
        tenth = self.screenh // 10
        pos = self.screenh - tenth
        while pos >=0:
            poslist.append(pos)
            pos -= tenth
        return poslist

    def get_screensyls(self):
        #selfsyls = list(map(lambda a: a if a.visible == True else self.tempsyl(a.rect), self.syls))
        syls = self.syls[self.cs:] + self.syls[:self.cs]
        liste = syls[:len(self.poslist)] # takes however much is left if under the need
        if len(liste) < len(self.poslist):
            diff = len(self.poslist)-len(liste)
            while diff:
                temp = self.generated
                liste.append(temp)
                diff -= 1
        return liste

    def blitloop(self):
        self.screensyls = self.get_screensyls()
        self.screen.fill(self.black)
        print(len(self.syls),self.cs)
        for i in range(len(self.poslist)):
            if self.screensyls:
                syl = self.screensyls.pop(0)
                if syl.visible == True:
                    self.screen.blit(syl.image, (syl.rect.x, self.poslist[i]+self.counter))
                else:
                    self.screen.blit(self.invisible,(syl.rect.x, self.poslist[i]+self.counter))
                syl.rect.y = self.poslist[i] + self.counter
        self.counter += 5
        if self.counter == self.screenh // 10:
            self.counter = 0
            self.cs += 1
            if self.cs > len(self.syls)-1: # == doesn't catch after deleted words
                self.cs = 0
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.flip()

    def gameloop(self):
        clock = pg.time.Clock()
        run = True
        print([each.name for each in self.words])
        loops = 0
        click = False
        while True:
            clock.tick(self.fps) #ONE LOOP
            self.score -= 0.005 #quicker play wins more
            for stuff in event.get(): # CAN QUIT ONCE A LOOP
                if stuff.type == QUIT:
                    self.screen.fill(self.black)
                    image_end = self.font.render("GAME OVER", False, self.white)
                    image_end_rect = image_end.get_rect()
                    image_end_rect.center = self.screen.get_rect().center
                    self.screen.blit(image_end, image_end_rect)
                    display.flip()
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
                    if len(self.syls)==0: # including the invisible ones
                        self.screen.fill(self.black)
                        image_win = self.bigfont.render(f'YOU WON!', False, self.white)
                        image_score = self.bigfont.render(f'YOUR SCORE IS {round(self.score, 3)}', False, self.white)
                        image_win_rect = image_win.get_rect()
                        image_score_rect = image_score.get_rect()
                        image_win_rect.center = self.screen.get_rect().center
                        image_score_rect.center = self.screen.get_rect().center
                        image_score_rect.y += image_win_rect.h * 1.5
                        self.screen.blit(image_win, image_win_rect)
                        self.screen.blit(image_score, image_score_rect)
                        display.flip()
                        time.wait(3000)
                        exit()
                    else:
                        action = self.player.act() # PLAYER MOVES ONCE A LOOP
                        if action == 1: #how does this work again? return is false
                            run = False
                        self.player.pick(self.syls)
                        self.blitloop()
                else:
                    self.desk(click)
                    click = False
