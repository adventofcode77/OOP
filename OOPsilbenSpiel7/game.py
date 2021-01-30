import pygame as pg
from pygame import *
from pygame.locals import *

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


    def draw_desk(self): # origs
        x,y = self.right,self.down
        sylobjects = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(sylobjects):
                    syl = sylobjects[index]
                    copy = silbe.Silbe(syl.inhalt, syl.word, syl.bit)
                    if syl.clicked_on == True:
                        copy.image = self.font.render(copy.inhalt,False,self.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        current_selected = ""
        # the event loop didn't work inside of this function
        self.screen.fill(self.lila)
        syls = self.draw_desk() # copies
        if click:
            x,y = click
            for syl in syls:
                if syl.rect.collidepoint(x,y):
                    print("player collides with syl")
                    for item in self.player.my_silben: #next()?
                        if item.inhalt == syl.inhalt:
                            if item.clicked_on:
                                print("clicked off", item.inhalt)
                                item.clicked_on = False
                                for i in range(len(self.player.appendlist)-1):
                                    each = self.player.appendlist[i]
                                    if each.bit == item.bit:
                                        del self.player.appendlist[i]
                            else:
                                item.clicked_on = True
                                print("clicked on",item.inhalt)
                                self.draw_word(syl)
        self.draw_word()
        display.flip()


    def draw_word(self,syl=None):
        self.blitword(self.lila) #draws over word and def
        if self.deleted_word_bool:
            self.player.appendlist = []
            print("a word has just been deleted")
        if syl:
            self.player.appendlist.append(syl)
            for syl in self.player.appendlist:
                print(syl.inhalt)
        self.blitword(self.black)
        defstring = self.makedefstring()
        self.check_word(defstring)

    def makedefstring(self):
        liste = []
        bitlists = [a.bit for a in self.player.appendlist]
        bitstrings = map(" ".join, bitlists)
        defstring = " ".join(bitstrings)
        return defstring

    def blitword(self,farbe):
        wordstring = "".join([a.inhalt for a in self.player.appendlist])
        defstring = self.makedefstring()
        word_image = self.font.render(wordstring, False, farbe)
        def_image = self.font.render(defstring, False, farbe)
        ww, wh = self.font.size(self.player.wordlist)
        dw, dh = self.font.size(self.player.deflist)
        self.screen.blit(word_image, ((self.screenw - ww) // 2, self.down * 6))
        self.screen.blit(def_image, ((self.screenw - dw) // 2, self.down * 7))

    def check_word(self, defstring):
        selfwordsdef = [a.meaning for a in self.words]
        if defstring in selfwordsdef or defstring[:-1] in selfwordsdef:
            indexword = selfwordsdef.index(defstring)
            self.delete_word(indexword)

    def delete_word(self,indexword): #same syl is actually different objects in different lists, why?
        self.score += 5
        self.counter -= 1
        for silbe in self.player.appendlist:
            for syl in self.syls:
                if silbe.name == syl.name and silbe.bit == syl.bit:
                    indexsyl = self.syls.index(syl)
                    del self.syls[indexsyl]
            for syl in self.player.my_silben:
                if silbe.name == syl.name and silbe.bit == syl.bit:
                    indexsyl = self.syls.index(syl)
                    del self.syls[indexsyl]
        self.blitword(self.gold)
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
                            self.player.wordlist = ""
                            self.player.deflist = ""
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
                        except:
                            print("list index out of range")
                            print("length of list",len(self.syls))
                            print("index",self.counter)
                            if len(self.syls) == 0:
                                image_win = self.bigfont.render(f'YOU WON! YOUR SCORE IS {self.score}', False, self.white)
                                x, y, image_w, h = image_newloop.get_rect()
                                self.screen.blit(image_win, (self.screenw // 2 - image_w // 2, self.screenh // 2))
                else:
                    self.desk(click)
                    click = False
