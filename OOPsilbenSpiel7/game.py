import pygame as pg
from pygame import *
from pygame.locals import *
import random
from OOPsilbenSpiel7 import woerter
from OOPsilbenSpiel7 import globale_variablen
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import gameloop


class Game(globale_variablen.Settings):
    def __init__(self, input_code):
        super().__init__()
        self.input_code = input_code
        self.output_code = ""
        self.player = spieler.Spieler(self) # takes the game object as parameter
        self.woerter = woerter.Woerter(self, input_code)
        self.words = self.woerter.words
        self.score = 0
        syls = self.woerter.silben + self.woerter.code_syls
        self.syls = random.sample(syls, len(syls))
        #self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.syl_speed = 0
        self.deleted_word_bool = False
        self.deleted_code_word_bool = False
        self.deletedlist = []
        self.deleted_word = ""
        self.start_syls_cut_at = 0
        self.pos_list = self.get_pos_list()
        self.screen_syls = self.get_screensyls()
        self.guessed_code_words = []
        #gameloop should run last
        self.gameloop = gameloop.Gameloop(self) # starts the game

    def desk(self,click):
        # the event loop didn't work inside of this function
        self.screen_copy.fill(self.black)
        syls = self.draw_desk() # copies
        if click:
            x,y = click
            for syl in syls:
                if syl.rect.collidepoint(x,y):
                    for item in self.player.my_silben: #next()?
                        if item.tuple == syl.tuple:
                            # couldn't find syl objects in lists where i'd previously put them (& collidelist didn't work)
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

    def draw_desk(self): # origs
        mysilben = self.player.my_silben
        desk_syls = []
        index = 0
        for y in range(self.down,self.down*4,self.down):
            for x in range(self.right,self.right*5,self.right):
                if index < len(mysilben):
                    syl = mysilben[index]
                    copy = silbe.Silbe(syl.inhalt, syl.word, syl.bit, syl.tuple[0], syl.tuple[1], syl.info, syl.rgb)
                    # why didn't syl.copy() work?
                    if syl.clicked_on == True:
                        copy.image = self.default_font.render(copy.inhalt, False, self.lime)
                    else:
                        copy.image = self.default_font.render(copy.inhalt, False, self.white)
                    copy.rect.x,copy.rect.y = x,y
                    self.screen_copy.blit(copy.image, copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls

    def draw_word(self,syl=None):
        if syl:
            self.blit_word(farbe=(self.lila, self.lila)) #draws over word and def
            self.player.appendlist.append(syl)
            if self.deleted_word_bool or self.deleted_code_word_bool:
                self.deleted_word_bool = False
                self.deleted_code_word_bool = False
                self.deletedlist = []
                self.deleted_word = ""
            self.check_word()
        self.blit_word()

    def make_def_list(self):
        if self.deleted_word_bool or self.deleted_code_word_bool:
            bitlists = [word for a in self.deletedlist[:] for word in a.bit]
        else:
            bitlists = [word for a in self.player.appendlist[:] for word in a.bit]
        return bitlists

    def blit_word(self, farbe=None): # replace with a pygame gui that works with sql? or word by word? # None due to self.colors not working
        if farbe is not (self.lila, self.lila):
            if self.deleted_word_bool:
                farbe = (self.purple, self.purple)
                wordstring = self.deleted_word
            elif self.deleted_code_word_bool:
                farbe = (self.yellow, self.yellow)
                wordstring = self.deleted_word
            else:
                farbe = (self.lime, self.cyan)
                wordstring = "".join([a.inhalt for a in self.player.appendlist])
        self.blit_string_word_by_word(self.make_def_list(), farbe[1], self.screen_copy.get_rect().center)
        word_image = self.default_font.render(wordstring, False, farbe[0])
        wordrect = word_image.get_rect()
        wordrect.center = self.screen_copy.get_rect().center
        self.screen_copy.blit(word_image, (wordrect.x, wordrect.y))

    def blit_string_word_by_word(self, defstring, color, midtop, font = None,screen=None):  # does it need to get the image in order to know how big the font i
        words = defstring
        line = ""
        list_lines_img = []
        height,width = 0,0
        if font is None:
            font = self.smaller_font
        if not screen:
            screen = self.screen_copy
        for i in range(len(words)):
            word = words[i]
            line += word + " "
            line_img = font.render(line, False, color)
            if line_img.get_rect().w >= 0.5 * self.screen_copy.get_rect().w:
                list_lines_img.append(line_img)
                line = ""
            elif i == len(words)-1: # append the last part
                list_lines_img.append(line_img)
            height,width = line_img.get_rect().h, line_img.get_rect().w
        spacing = height
        last_line_y = 0
        for i in range(len(list_lines_img)):
            line_img = list_lines_img[i]
            line_rect = line_img.get_rect()
            line_rect.center = (midtop[0], (midtop[1] + spacing * (i + 1)))  # spacing needs to increase with each line
            screen.blit(line_img, line_rect)
            last_line_y = line_rect.y
        return last_line_y # how far down the screen there is curently text

    def check_word(self):
        temp_bool = True
        appendlisttuples = [a.tuple for a in self.player.appendlist]
        for word in self.words: # check for the word in non-code words
            wordtuples = [a.tuple for a in word.syls] # 1 comparison with wordtuples for each word in words
            if appendlisttuples == wordtuples:
                self.deleted_word = word.name
                self.delete_word()
                self.words.remove(word) # words is used only for cheating
                self.deleted_word_bool = True
                temp_bool = False
        if temp_bool:
            for word in self.woerter.code_words: # check in code words
                wordtuples = [a.tuple for a in word.syls]
                if appendlisttuples == wordtuples:
                    self.deleted_word = word.name
                    self.delete_word()
                    self.woerter.code_words.remove(word)
                    self.guessed_code_words.append(word)
                    self.deleted_code_word_bool = True

    def delete_word(self): #same syl is actually different objects in different lists, why?
        self.score += 5
        for this in self.player.appendlist:
            for syl in self.syls:
                if this.tuple == syl.tuple:
                    index = self.syls.index(syl)
                    if len(self.syls) <len(self.pos_list):
                        replacement = silbe.Silbe("o", "word", ["bit"], 404, 404, self, (0,0,0)) # replace with simpler object?
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


    def get_pos_list(self):
        poslist = []
        tenth = self.screenh // 10
        pos = self.screenh - tenth
        while pos >=0-self.syl_speed:
            poslist.append(pos)
            pos -= tenth
        return poslist

    def get_screensyls(self):
        syls = self.syls[self.start_syls_cut_at:] + self.syls[:self.start_syls_cut_at]
        return syls[:len(self.pos_list)] # (now syls should always be bigger than this cut)

    def blit_loop(self): # why is there some trembling? especially after downsizing screen
        self.screen_syls = self.get_screensyls()
        self.screen_copy.fill(self.black)
        for i in range(len(self.pos_list)):
            if self.screen_syls:
                syl = self.screen_syls.pop(0)
                if syl.visible == True:
                    self.screen_copy.blit(syl.image, (syl.rect.x, self.pos_list[i] + self.syl_speed))
                else:
                    self.screen_copy.blit(self.invisible, (syl.rect.x, self.pos_list[i] + self.syl_speed))
                syl.rect.y = self.pos_list[i] + self.syl_speed
        self.syl_speed += self.screenh // 100
        if self.syl_speed >= self.screenh // 10:
            self.syl_speed = 0
            self.start_syls_cut_at += 1
            if self.start_syls_cut_at > len(self.syls)-1: # "==" doesn't work after words get deleted
                self.start_syls_cut_at = 0
        self.screen_copy.blit(self.player.image, self.player.rect)
        self.screen_transfer()

    def screen_transfer(self): # corrently resizes the current display image, but objects are no longer clickable at the right coordinates
        resized_screen_copy = pg.transform.scale(self.screen_copy, self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()


