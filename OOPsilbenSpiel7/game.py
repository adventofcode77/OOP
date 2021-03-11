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
    def __init__(self, input_code):
        super().__init__()
        self.input_code = input_code
        self.output_code = ""
        self.syl_speed_change = 10
        self.initial_syl_speed_change = self.syl_speed_change
        # variables above are needed to initialise other classes' instances
        self.player = spieler.Spieler(self) # takes the game object as parameter
        self.woerter = woerter.Woerter(self, input_code)

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
        self.corrected_subsurface = self.screen_copy.copy()
        self.padding = 0
        self.menu = menu.Menu(self)
        #gameloop should run last
        self.gameloop = gameloop.Gameloop(self) # starts the game

    def desk(self,click): # the click is adjusted for where it'd be on screen_copy
        # the event loop didn't work inside of this function
        self.screen_copy.fill(self.black)
        self.large_surface.fill(self.black)
        syls,surface_cut = self.draw_desk() # copies; copy of the desk surface so far (syls are hardcoded on surface cut)
        if click:
            click = self.scale_click(click,self.corrected_subsurface,self.screen_copy)
            x,y = click
            x -= self.padding # change padding back to 0 when the text no longer goes over the original screen size
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
                                self.draw_word(surface_cut,syl)
        self.draw_word(surface_cut)

    def draw_desk(self): # origs
        surface_cut = pg.Surface.subsurface(self.large_surface,pg.Rect(2000,0,3000,3000))
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
                    surface_cut.blit(copy.image, copy.rect)
                    desk_syls.append(copy) #copy whole syl
                    index += 1
                    x += copy.rect.w
        return desk_syls, surface_cut

    def draw_word(self,surface_cut,syl=None):
        if syl:
            self.blit_word(surface_cut,farbe=(self.lila, self.lila)) #draws over word and def
            self.player.appendlist.append(syl)
            if self.deleted_word_bool or self.deleted_code_word_bool:
                self.deleted_word_bool = False
                self.deleted_code_word_bool = False
                self.deletedlist = []
                self.deleted_word = ""
            self.check_word()
        self.blit_word(surface_cut)

    def make_def_list(self):
        if self.deleted_word_bool or self.deleted_code_word_bool:
            bitlists = [word for a in self.deletedlist[:] for word in a.bit]
        else:
            bitlists = [word for a in self.player.appendlist[:] for word in a.bit]
        return bitlists

    def blit_word(self, surface_cut,farbe=None): # replace with a pygame gui that works with sql? or word by word? # None due to self.colors not working
        height_of_all = 0
        #self.large_surface.fill(self.white) #check this
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
        blit_h = self.blit_string_words(self.make_def_list(), farbe[1], self.screen_copy.get_rect().center, screen=surface_cut) # starts one line below the blitted word per the function
        height_of_all = blit_h
        word_image = self.default_font.render(wordstring, False, farbe[0])
        wordrect = word_image.get_rect()
        wordrect.center = self.screen_copy.get_rect().center
        surface_cut.blit(word_image, (wordrect.x, wordrect.y))
        self.text_wrap(self.screen_copy,self.large_surface,self.identation_surface_cut,height_of_all)

    def text_wrap(self, screen_copy,large_surface,right_identation_l_s,text_h):
        orig_text_w,orig_text_h = screen_copy.get_rect().w,screen_copy.get_rect().h
        if text_h > screen_copy.get_rect().h:
            new_text_h = text_h
        else:
            new_text_h = orig_text_h
        ratio = new_text_h / orig_text_h
        new_text_w = orig_text_w * ratio
        self.padding = (new_text_w - orig_text_w) // 2 # indents the cut to the left so the new width can take black background proportionately from left and right
        self.corrected_subsurface = pg.Surface.subsurface(large_surface,pg.Rect((right_identation_l_s - self.padding,0,new_text_w,new_text_h)))
        self.resized_copied_surface = pg.transform.scale(self.corrected_subsurface, (screen_copy.get_rect().w,screen_copy.get_rect().h))
        screen_copy.blit(self.resized_copied_surface,(0,0))

    def blit_string_words(self, list_ps, color, midtop, font = None, screen=None):  # does it need to get the image in order to know how big the font i
        words = list_ps
        line = ""
        list_lines_img = []
        height,width = 0,0
        color_copy = color
        if font is None:
            font = self.smaller_font
        if not screen:
            screen = self.screen_copy
        for i in range(len(words)):
            word = words[i]
            if word.isupper() or word[0].isdigit():
                color = self.lime
            line += word + " "
            line_img = font.render(line, False, color)
            if line_img.get_rect().w >= 0.5 * self.screen_copy.get_rect().w:
                list_lines_img.append(line_img)
                line = ""
                color = color_copy
            elif i == len(words)-1:
                list_lines_img.append(line_img) # append the last part
            height,width = line_img.get_rect().h, line_img.get_rect().w
        spacing = height
        last_line_y = 0
        for i in range(len(list_lines_img)):
            line_img = list_lines_img[i]
            line_rect = line_img.get_rect()
            line_rect.center = (midtop[0], (midtop[1] + spacing * (i + 1)))  # spacing needs to increase with each line
            screen.blit(line_img, line_rect)
            last_line_y = line_rect.y
        return last_line_y+spacing # how far down the screen there is curently text

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


