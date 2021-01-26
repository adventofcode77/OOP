import pygame as pg
from pygame import *
from pygame.locals import *

from OOPsilbenSpiel7 import bank
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler


class Game:

    def __init__(self):
        self.settings = setup.Settings()
        self.player = spieler.Spieler()
        print("works before bank init")
        self.bank = bank.Bank()
        self.words = self.bank.get_words()
        self.txt_syls = self.bank.txtsyls
        self.selected = []
        self.font = pg.font.SysFont("Arial",20)
        self.bigfont = pg.font.SysFont("Arial",30)
        self.txt = self.font.render("player",False,self.settings.black)
        self.sprites = sprite.Group()
        self.screen = pg.display.set_mode((self.settings.screenh,self.settings.screenw))


    def draw_desk(self): # origs
        x,y = self.settings.right,self.settings.down
        sylobjects = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.settings.down,self.settings.down*4,self.settings.down):
            for x in range(self.settings.right,self.settings.right*5,self.settings.right):
                if index < len(sylobjects):
                    syl = sylobjects[index]
                    copy = silbe.Silbe(syl.inhalt,syl.word,syl.bit)
                    if syl.on == True:
                        #print("syl on")
                        copy.image = self.font.render(copy.inhalt,False,self.settings.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.screen.blit(copy.image,copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def desk(self,click):
        # the event loop didn't work inside of this function
        self.screen.fill(self.settings.lila)
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
        word_image = self.font.render(word,False,self.settings.black)
        def_image = self.font.render(definition,False,self.settings.black)
        ww,wh = self.font.size(word)
        dw,dh = self.font.size(definition)
        self.screen.blit(word_image,((self.settings.screenw-ww)//2,self.settings.down*6))
        self.screen.blit(def_image,((self.settings.screenw-dw)//2,self.settings.down*7))
        self.player.word = word

    def check_word(self):
        if self.player.word in self.words:
            if all(a.word == self.player.selected[0].word for a in self.player.selected):
                correct_image = self.font.render("correct",False,self.settings.white)
                cw,ch = self.font.size("correct")
                self.screen.blit(correct_image,((self.settings.screenw-cw)//2,self.settings.down*7))
                print("correct")


    def screen_update_and_move(self,allsyls,current_syl,player): # after every changed object
        self.screen.fill(self.settings.zuff)
        for i in range(current_syl):
            syllable = allsyls[i]
            if syllable.visible == True:
                self.screen.blit(syllable.image,syllable.rect) #draw function?
            syllable.rect.y += syllable.speed
        self.screen.blit(player.image,player.rect)
        pg.display.flip()

    def gameloop(self):
        self.sprites.add(self.bank.words)
        clock = pg.time.Clock()
        run = True
        print([each.name for each in self.words])
        sylobjects = self.bank.silben
        loops = 0
        counter = 0
        click = False
        bool = False
        boolcounter = 0
        while True:
            clock.tick(self.settings.fps) #ONE LOOP
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
                            self.screen.fill(self.settings.black)
                            boolcounter += 1
                            self.screen.blit(self.bigfont.render("new loop",False,self.settings.white),(200,250))
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
                        self.screen_update_and_move(sylobjects,counter,self.player)
                else:
                    self.desk(click)
                    click = False
