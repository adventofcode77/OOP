import pygame as pg
from pygame import *
from pygame.locals import *
import random
from OOPsilbenSpiel7 import woerter
from OOPsilbenSpiel7 import globale_variablen
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler
from OOPsilbenSpiel7 import gameloop
from OOPsilbenSpiel7 import menu


class Game(globale_variablen.Settings):
    def __init__(self, input_codes, file_paths, binary_code):
        super().__init__()
        self.binary_code = binary_code
        self.input_codes = input_codes
        self.output_code = ""
        self.next_counter = 0
        self.test_next_counter = 0
        self.menu = menu.Menu(self)
        self.language = 1 # self.choose_language()
        self.file_path = file_paths[self.language-1]
        self.syl_speed_change = 10
        self.initial_syl_speed_change = self.syl_speed_change
        # variables above may be needed to initialise other classes' instances
        self.player = spieler.Spieler(self) # takes the game object as parameter
        self.woerter = woerter.Woerter(self)
        self.words = self.woerter.words
        self.score = 0
        syls = self.woerter.silben + self.woerter.code_syls
        self.syls = random.sample(syls, len(syls))
        #self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.syl_pos_change = 0
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

    def choose_language(self):
        while True:
            self.menu.choose_language()
            for ev in event.get():
                if ev.type == KEYDOWN:
                    if ev.key == K_d:
                        return 1
                    elif ev.key == K_e:
                        return 2

    def desk(self,click): # the click is adjusted for where it'd be on screen_copy
        # the event loop didn't work inside of this function
        self.screen_copy.fill(self.black)
        syls = self.draw_desk() # copies; copy of the desk surface so far (syls are hardcoded on surface cut)
        if click:
            click = self.scale_click(click,self.screen_copy,self.screen_copy)
            x,y = click
            for syl in syls:
                #print(syl.inhalt,syl.rect.x,syl.rect.y)
                if syl.rect.collidepoint(x,y):
                    for item in self.player.my_silben: #next()?
                        if item.tuple == syl.tuple: # couldn't find syl objects in lists where i'd previously put them (& collidelist didn't work)
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
                    if syl.clicked_on:
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
            #self.blit_word(farbe=(self.lila, self.lila)) #draws over word and def
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

    def blit_word(self, surface=None, farbe=None): # replace with a pygame gui that works with sql? or word by word? # None due to self.colors not working
        if self.deleted_word_bool:
            farbe = (self.purple, self.purple)
            word_string = self.deleted_word
        elif self.deleted_code_word_bool:
            farbe = (self.yellow, self.yellow)
            word_string = self.deleted_word
        else:
            farbe = (self.lime, self.cyan)
            word_string = "".join([a.inhalt for a in self.player.appendlist])
        if not surface:
            surface = self.screen_copy
        word_image = self.default_font.render(word_string, False, farbe[0])
        word_rect = word_image.get_rect()
        word_rect.center = self.screen_copy.get_rect().center
        surface.blit(word_image, (word_rect.x, word_rect.y))
        height_of_all = word_rect.y + self.font_spacing(self.default_font)
        blit_h = self.blit_string_words(self.make_def_list(), farbe[1], (self.screen_copy.get_rect().center[0],height_of_all), screen=surface) # starts one line below the blitted word per the function

    def blit_string_words(self, lst, color, midtop, font = None, screen=None):  # does it need to get the image in order to know how big the font i
        window_counter = 0
        if not screen:
            screen = self.screen_copy
        screen_rect = screen.get_rect()
        copy_screen = screen.copy()
        list_snapshots_to_blit = {}
        words = lst
        if type(words) == str:
            words = words.split()
        color_copy = color
        if font is None:
            font = self.smaller_font
        spacing = self.font_spacing(font)
        last_line_down = midtop[1]
        last_word_right = 0.25 * copy_screen.get_rect().w
        for i in range(len(words)):
            word = words[i]
            if word.isupper() or word[0].isdigit():
                color = self.lime
            word_img = font.render(word+" ", False, color)
            word_rect = word_img.get_rect()
            color = color_copy
            if last_word_right >= 0.75 * copy_screen.get_rect().w:
                if last_line_down < screen_rect.h-spacing*3: # twice the highest spacing?
                    last_word_right = 0.25 * copy_screen.get_rect().w
                    last_line_down += spacing
                    copy_screen.blit(word_img, (last_word_right,last_line_down))
                    last_word_right += word_rect.w
                else:
                    copy_screen = screen.copy()
                    last_line_down = midtop[1]
                    last_word_right = 0.25 * copy_screen.get_rect().w
                    window_counter += 1
                    copy_screen.blit(word_img, (last_word_right,last_line_down))
                    last_word_right += word_rect.w
            else:
                copy_screen.blit(word_img, (last_word_right,last_line_down))
                last_word_right += word_rect.w
            if word[-1] in ".!?":
                last_word_right = 0.25 * copy_screen.get_rect().w
                last_line_down += spacing * 1.5
            list_snapshots_to_blit[window_counter] = copy_screen.copy()
        if len(list_snapshots_to_blit) == 0:
            list_snapshots_to_blit[window_counter] = screen.copy()
        if self.test_next_counter< 0: # temp? counter adjusts the text window counter without changing it, so that it doesnt keep resetting to the first or last window when it's outside the bounds
            temp_counter = len(list_snapshots_to_blit)-1 - (self.test_next_counter % len(list_snapshots_to_blit))
        else:
            temp_counter = self.test_next_counter % len(list_snapshots_to_blit)
        screen.blit(list_snapshots_to_blit[temp_counter],(0,0))
        return last_line_down + self.font_spacing(font) # how far down the screen there is curently text

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
        while pos >=0-self.syl_pos_change:
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
                    self.screen_copy.blit(syl.image, (syl.rect.x, self.pos_list[i] + self.syl_pos_change))
                else:
                    self.screen_copy.blit(self.invisible, (syl.rect.x, self.pos_list[i] + self.syl_pos_change))
                syl.rect.y = self.pos_list[i] + self.syl_pos_change
        self.syl_pos_change += int((self.screenh / 1000) * self.syl_speed_change)
        # print("syl pos change", self.syl_pos_change,"speed change",self.syl_speed_change,"rest",self.screenh/1000)
        # print("syl speed change",self.syl_speed_change)
        if self.syl_pos_change >= self.screenh // 10:
            self.syl_pos_change = 0
            self.start_syls_cut_at += 1
            if self.start_syls_cut_at > len(self.syls)-1: # "==" doesn't work after words get deleted
                self.start_syls_cut_at = 0
        elif self.syl_pos_change <= - self.screenh // 10:
            self.syl_pos_change = 0
            self.start_syls_cut_at -= 1
            if self.start_syls_cut_at < 1: # "==" doesn't work after words get deleted
                self.start_syls_cut_at = len(self.syls)-1
        self.screen_copy.blit(self.player.image, self.player.rect)
        self.screen_transfer()

    def screen_transfer(self): # corrently resizes the current display image, but objects are no longer clickable at the right coordinates
        resized_screen_copy = pg.transform.scale(self.screen_copy, self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()


