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


    def draw_desk(self): # origs
        x,y = self.right,self.down
        sylobjects = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(sylobjects):
                    syl = sylobjects[index]
                    copy = silbe.Silbe(syl.inhalt,syl.word,syl.bit)
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
                            item.clicked_on = True
                            #print(item.inhalt," on")
                    self.player.selected.append(syl)
                    current_selected = syl
                    print("selected takes that syl",len(self.player.selected))
        if current_selected:
            self.draw_word(current_selected)
        self.check_word()
        display.update()


    def draw_word(self,syl):
        print("self player selected arrives at draw word",self.player.selected)
        self.player.word += f' {syl.inhalt}'
        self.player.definition += " ".join(syl.bit) + " "
        print("player def after adding all syls",self.player.definition)
        word_image = self.font.render(self.player.word,False,self.black)
        def_image = self.font.render(self.player.definition,False,self.black)
        ww,wh = self.font.size(self.player.word)
        dw,dh = self.font.size(self.player.definition)
        self.screen.blit(word_image,((self.screenw-ww)//2,self.down*6))
        self.screen.blit(def_image,((self.screenw-dw)//2,self.down*7))

    def delete_word(self): #same syl is actually different objects in different lists, why?
        self.score += 5
        nurdefs = [a.meaning for a in self.words]
        indexword = nurdefs.index(self.player.definition.split())  # same place as in words but def only
        guessedword = self.words[indexword]
        indexinmysyls = self.player.my_silben.index(guessedword)
        print("len before",len(self.player.my_silben))
        del self.player.my_silben[indexinmysyls]
        print("len after", len(self.player.my_silben))
        for syl in guessedword.syls:
            print(syl)
            print(syl.inhalt)
            onlythebits = [a.bit for a in self.syls]
            if syl.bit in onlythebits:
                indexsyl = onlythebits.index(syl.bit)
                del self.syls[indexsyl]

    def check_word(self):
        if self.player.definition.split() in [a.meaning for a in self.words]:
            self.delete_word()
        elif self.player.definition[:-1] == " ":
            self.delete_word()
        else:
            print(f'incorrect,{self.player.definition.split()} is not in any of:\n {[a.meaning for a in self.words]}\n')


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
        counter = 0
        click = False
        bool = False
        boolcounter = 0
        while True:
            clock.tick(self.fps) #ONE LOOP
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
                            if counter+1 == len(self.syls):
                                print("counter resets")
                                for syl in self.syls:
                                    syl.rect.y = 0
                                counter = 0
                                bool = True
                            counter += 1
                            loops = 0
                        loops += 1
                        try:
                            self.screen_update_and_move(self.syls,counter,self.player)
                        except:
                            print("list index out of range")
                            print("length of list",len(self.syls))
                            print("index",counter)
                else:
                    self.desk(click)
                    click = False
