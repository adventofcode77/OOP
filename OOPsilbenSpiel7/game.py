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
from OOPsilbenSpiel7 import word

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
        self.buttons = []
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
        self.screen_copy.fill(self.black)
        height_of_all = self.draw_desk()
        if click:
            click = self.scale_click(click,self.screen_copy,self.screen_copy)
            x,y = click
            for syl_button in self.buttons:
                if syl_button.rect.collidepoint(x,y):
                    syl = self.player.my_silben[syl_button.index]
                    if syl.clicked_on:
                        syl.clicked_on = False
                        index = self.player.appendlist.index(syl)
                        del self.player.appendlist[index]
                    else:
                        syl.clicked_on = True
                        self.draw_word(height_of_all, syl)

        self.draw_word(height_of_all)

    def draw_desk(self):
        blit_h = self.blit_clickable_words(self.player.my_silben, self.white,(0,self.down),space_after_word="  ",no_buttons=False)
        return blit_h

    def draw_word(self,height_of_all,syl=None):
        if syl:
            #self.blit_word(farbe=(self.lila, self.lila)) #draws over word and def
            self.player.appendlist.append(syl)
            if self.deleted_word_bool or self.deleted_code_word_bool:
                self.deleted_word_bool = False
                self.deleted_code_word_bool = False
                self.deletedlist = []
                self.deleted_word = ""
            self.check_word()
        self.blit_word(height_of_all)

    def make_def_list(self):
        if self.deleted_word_bool or self.deleted_code_word_bool:
            bitlists = [word for a in self.deletedlist[:] for word in a.bit]
        else:
            bitlists = [word for a in self.player.appendlist[:] for word in a.bit]
        return bitlists

    def blit_word(self, height_of_all,surface=None, farbe=None): # replace with a pygame gui that works with sql? or word by word? # None due to self.colors not working
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
        word_image = self.default_font.render(word_string, True, farbe[0])
        word_rect = word_image.get_rect()
        word_rect.centerx, word_rect.y = self.screen_copy.get_rect().centerx, height_of_all
        surface.blit(word_image, word_rect)
        height_of_all = word_rect.y + self.font_spacing(self.default_font)
        blit_h = self.blit_clickable_words(self.make_def_list(), farbe[1], (self.screen_copy.get_rect().center[0], height_of_all), screen=surface) # starts one line below the blitted word per the function

    def blit_clickable_words(self, lst, color, midtop, font = None, screen=None, space_after_word=" ",no_buttons = True):  # does it need to get the image in order to know how big the font i
        window_counter = 0
        if not screen:
            screen = self.screen_copy
        screen_rect = screen.get_rect()
        copy_screen = screen.copy()
        list_snapshots_to_blit = {}
        words = lst
        if no_buttons:
            copy_buttons = self.buttons[:]
        self.buttons = []
        if type(words) == str:
            words = words.split()
        color_copy = color
        if font is None:
            font = self.smaller_font
        spacing = self.font_spacing(font)
        last_line_down = midtop[1]
        last_word_right = 0.25 * copy_screen.get_rect().w
        for i in range(len(words)):
            aword = words[i]
            if type(aword) is word.Word:
                if aword.color:
                    color = aword.color
                    aword = aword.name
            elif type(aword) is silbe.Silbe:
                color = self.lime if aword.clicked_on else self.white
                aword = aword.inhalt
            elif aword.isupper() or aword[0].isdigit():
                color = self.lime
            word_img = font.render(aword+space_after_word, True, color)
            word_rect = word_img.get_rect()
            color = color_copy
            if last_word_right >= 0.75 * copy_screen.get_rect().w:
                if last_line_down < screen_rect.h-spacing*3: # twice the highest spacing?
                    last_word_right = 0.25 * copy_screen.get_rect().w
                    last_line_down += spacing
                    word_rect.x, word_rect.y = last_word_right,last_line_down
                    self.buttons.append(word.Button(aword,word_img, word_rect,i))
                    copy_screen.blit(word_img, word_rect)
                    last_word_right += word_rect.w
                else:
                    copy_screen = screen.copy()
                    last_line_down = midtop[1]
                    last_word_right = 0.25 * copy_screen.get_rect().w
                    window_counter += 1
                    word_rect.x, word_rect.y = last_word_right, last_line_down
                    self.buttons.append(word.Button(aword,word_img, word_rect,i))
                    copy_screen.blit(word_img, word_rect)
                    last_word_right += word_rect.w
            else:
                word_rect.x, word_rect.y = last_word_right, last_line_down
                self.buttons.append(word.Button(aword,word_img, word_rect,i))
                copy_screen.blit(word_img, word_rect)
                last_word_right += word_rect.w
            if aword[-1] in ".!?":
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
        if no_buttons:
            self.buttons = copy_buttons
        print("buttons", [(button.text, button.rect) for button in self.buttons])
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
        resized_screen_copy = pg.transform.smoothscale(self.screen_copy, self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()


