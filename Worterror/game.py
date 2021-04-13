import pygame as pg
from pygame import *
import random
import woerter, globale_variablen, silbe, spieler, gameloop, menu, word


class Game(globale_variablen.Settings):
    def __init__(self, input_codes, file_paths, binary_code):
        super().__init__()
        pg.font.init()
        self.radiuses = []
        self.blink_counter = 0
        self.top = 0
        self.gw,self.nw = None, None
        self.h = 8
        self.change_color = True
        self.wait = False
        self.won = False
        self.binary_code = binary_code
        self.input_codes = input_codes
        self.output_code = "Dame schlägt Bauer"
        self.next_counter = 0
        self.test_next_counter = 0
        self.menu = menu.Menu(self)
        self.language = 1  # self.choose_language()
        self.file_path = file_paths[self.language - 1]
        self.syl_speed_change = 10
        self.initial_syl_speed_change = self.syl_speed_change
        # variables above may be needed to initialise other classes' instances
        self.spieler = spieler.Spieler(self)  # takes the game object as parameter
        self.woerter = woerter.Woerter(self)
        self.words = self.woerter.words
        syls = self.woerter.silben + self.woerter.code_syls
        self.syls = random.sample(syls, len(syls))
        self.silben_copy,self.code_silben_copy = self.woerter.silben[:],self.woerter.code_syls[:]
        # self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.syl_pos_change = 0
        self.deleted_word_bool = False
        self.deleted_code_word_bool = False
        self.deletedlist = []
        self.deleted_word = ""
        self.start_syls_cut_at = 0
        self.pos_list = self.get_pos_list()
        print("len post list", len(self.pos_list))
        self.gold_syls, self.lila_syls = [], []
        self.end_first_screen_part = (self.screenw // 10) * ((len(self.gold_syls) // 10) + 1)
        self.start_third_screen_part = self.screenw - (self.screenw // 10) * (len(self.lila_syls) // 10 + 1)
        self.tript2 = self.screen_copy.subsurface(self.end_first_screen_part, 0,
                                                  self.start_third_screen_part - self.end_first_screen_part,
                                                  self.screenh)
        self.end_header = 0
        self.header = self.screen_copy.subsurface(0,0,self.screenw,self.end_header)
        self.screen_syls = self.get_screensyls()
        self.guessed_code_words = []
        self.buttons = []
        self.move_word = None
        self.step_fps = 1
        # gameloop should run last
        self.gameloop = gameloop.Gameloop(self)  # starts the game (and the object gameloop never gets created as long as the game runs)
        print("this line doesn't execute")

    def desk(self, click):  # the click is adjusted for where it'd be on screen_copy
        self.tript2.fill(self.black)
        self.nums()
        if click:
            x, y = click
            for syl in self.gold_syls + self.lila_syls:
                if syl.rect.collidepoint(x, y):
                    if syl.clicked_on:
                        syl.clicked_on = False
                        index = self.spieler.appendlist.index(syl)
                        del self.spieler.appendlist[index]
                    else:
                        syl.clicked_on = True
                        self.draw_word(height_of_all=self.top,syl=syl, screen=self.tript2)
        self.draw_word(height_of_all=self.top,screen=self.tript2)

    def draw_word(self, height_of_all=None, syl=None, screen=None):
        if not height_of_all:
            height_of_all = self.down
        if syl:
            self.spieler.appendlist.append(syl)
            if self.deleted_word_bool or self.deleted_code_word_bool:
                self.deleted_word_bool = False
                self.deleted_code_word_bool = False
                self.deletedlist = []
                self.deleted_word = ""
            self.check_word()
        if not screen:
            screen = self.screen_copy
        self.blit_word(height_of_all, surface=screen)

    def make_def_list(self):
        if self.deleted_word_bool or self.deleted_code_word_bool:
            bitlists = [word for a in self.deletedlist[:] for word in a.bit]
        else:
            bitlists = [word for a in self.spieler.appendlist[:] for word in a.bit]
        return bitlists

    def blit_word(self, height_of_all=0,
                  surface=None):  # replace with a pygame gui that works with sql? or word by word? # None due to self.colors not working
        if self.deleted_word_bool or self.deleted_code_word_bool:
            farbe = (self.yellow, self.yellow)
            word_string = self.deleted_word
        else:
            farbe = (self.lime, self.cyan)
            word_string = "".join([a.name for a in self.spieler.appendlist])
        if not surface:
            surface = self.screen_copy
        word_img = self.default_font.render(word_string, True, farbe[0])
        surface.blit(word_img, (
            surface.get_rect().center[0] - word_img.get_rect().w // 2, height_of_all + self.down))
        height_of_all += self.down * 2
        blit_h = self.blit_clickable_words(self.make_def_list(), farbe[1], (
            self.screen_copy.get_rect().center[0], max(self.screen_copy.get_rect().center[1], height_of_all)),
                                           screen=surface)  # starts one line below the blitted word per the function

    def blit_clickable_words(self, lst, color, midtop, afont=0, screen=None,
                             no_buttons=True):
        window_counter = 0
        if not screen:
            screen = self.screen_copy
        copy_screen = screen.copy()
        copy_screen_rect = copy_screen.get_rect()
        list_snapshots_to_blit = {}
        if no_buttons:
            copy_buttons = self.buttons[:]
        self.buttons = []
        if type(lst) == str:
            lst = lst.split(" ")
        color_copy = color
        if not afont:
            afont = self.smaller_font
        spacing = self.font_spacing(afont)
        last_line_down = midtop[1]
        last_word_right = 0.25 * copy_screen_rect.w
        for i in range(len(lst)):
            aword = lst[i]
            if not aword:
                continue
            if type(aword) is word.Word:
                if aword.color:
                    color = aword.color
                    print(aword.name,"color is",aword.color)
                    aword = aword.name
            elif aword.isupper() or aword[0].isdigit():
                color = self.lime
            word_img = afont.render(aword, True, color)
            word_rect = word_img.get_rect()
            color = color_copy
            if last_word_right >= 0.75 * copy_screen_rect.w:
                if last_line_down < copy_screen_rect.h - spacing * 3:  # twice the highest spacing?
                    last_word_right = 0.25 * copy_screen_rect.w
                    last_line_down += spacing
                else:
                    copy_screen = screen.copy()
                    last_line_down = midtop[1]
                    last_word_right = 0.25 * copy_screen_rect.w
                    window_counter += 1
            word_rect.x, word_rect.y = last_word_right, last_line_down
            self.buttons.append(word.Button(aword, word_img, word_rect, i))
            copy_screen.blit(word_img, word_rect)
            last_word_right = last_word_right + word_rect.w + self.default_space_w
            if aword[-1] in ".!?:":
                last_word_right = 0.25 * copy_screen_rect.w
                last_line_down += spacing * 1.5
            list_snapshots_to_blit[window_counter] = copy_screen.copy()
        if len(list_snapshots_to_blit) == 0:
            list_snapshots_to_blit[window_counter] = screen.copy()
        if self.test_next_counter < 0:  # temp? counter adjusts the text window counter without changing it, so that it doesnt keep resetting to the first or last window when it's outside the bounds
            temp_counter = len(list_snapshots_to_blit) - 1 - (self.test_next_counter % len(list_snapshots_to_blit))
        else:
            temp_counter = self.test_next_counter % len(list_snapshots_to_blit)
        screen.blit(list_snapshots_to_blit[temp_counter], (0, 0))
        if no_buttons:
            self.buttons = copy_buttons
        return last_line_down + self.font_spacing(afont)  # how far down the screen there is curently text

    def check_word(self):
        temp_bool = True
        appendlisttuples = [a.tuple for a in self.spieler.appendlist]
        for word in self.words:  # check for the word in non-code words
            wordtuples = [a.tuple for a in word.syls]  # 1 comparison with wordtuples for each word in words
            if appendlisttuples == wordtuples:
                self.deleted_word = word.name
                self.delete_word()
                self.words.remove(word)  # words is used only for cheating
                self.deleted_word_bool = True
                temp_bool = False
        if temp_bool:
            for word in self.woerter.code_words:  # check in code words
                wordtuples = [a.tuple for a in word.syls]
                if appendlisttuples == wordtuples:
                    self.deleted_word = word.name
                    self.delete_word()
                    self.woerter.code_words.remove(word)
                    self.guessed_code_words.append(word)
                    self.deleted_code_word_bool = True

    def delete_word(self):  # same syl is actually different objects in different lists, why?
        for this in self.spieler.appendlist:
            for syl in self.syls:
                if this.tuple == syl.tuple:
                    index = self.syls.index(syl)
                    if len(self.syls) < len(self.pos_list):
                        replacement = silbe.Silbe("o", "word", ["bit"], 404, 404, self,
                                                  (0, 0, 0))  # replace with simpler object?
                        replacement.visible = False
                        replacement.rect.x,replacement.rect.y = 1,1
                        self.syls[index] = replacement
                    else:
                        self.syls.remove(syl)
                    self.sylscounter -= 1
            for syl in self.spieler.my_silben:
                if this.tuple == syl.tuple:
                    self.spieler.my_silben.remove(syl)
            for syl in self.gold_syls:
                if this.tuple == syl.tuple:
                    self.gold_syls.remove(syl)
            for syl in self.lila_syls:
                if this.tuple == syl.tuple:
                    self.lila_syls.remove(syl)
        self.deletedlist = self.spieler.appendlist[:]
        self.spieler.appendlist = []

    def get_pos_list(self):
        poslist = []
        tenth = self.screenh // self.h
        pos = self.screenh - tenth
        while pos >= 0 - self.syl_pos_change:
            poslist.append(pos)
            pos -= tenth
        return poslist

    def blink(self, num_steps, syl, new_color, start_color=None):
        if not start_color:
            start_color = syl.rgb
        list_ints = [
            int(orig_rgb_digit + (gold_rgb_digit - orig_rgb_digit) * self.step_fps / num_steps) for
            orig_rgb_digit, gold_rgb_digit in list(zip(start_color, new_color))]  # see stackoverflow link on fading
        try:
            list_ints[0], list_ints[1], list_ints[2] in range(0,255)
        except:
            print("excepted rgb for",syl.name,":",list_ints[0], list_ints[1], list_ints[2])
        if self.change_color: #step fps changes in the direction towards the new color
            if self.step_fps < num_steps: # self fps hasn't reached the new color yet
             self.step_fps += 1
            else: # the change is complete, but the bool shouldn't be flipped until a second has passed
                if not self.blink_counter: # blink counter starts counting for a second
                    self.blink_counter = 1
                elif self.blink_counter >= self.fps//2: # blink counter has finished counting for a time unit
                    self.change_color = False
        else:
            if self.step_fps > 0: # step fps is changing in the direction of the original color
                self.step_fps -= 1
            elif self.step_fps == 0:
                if not self.blink_counter:  # blink counter starts counting for a second
                    self.blink_counter = 1
                elif self.blink_counter >= self.fps//2: # blink counter has finished counting for a time unit
                    self.change_color = True
                    self.blink_counter = None # reset blink counter to None so it can start counting again at the right time
        return (list_ints[0], list_ints[1], list_ints[2])

    def get_screensyls(self):
        syls = self.syls[self.start_syls_cut_at:] + self.syls[:self.start_syls_cut_at]
        #syls = [syl for syl in syls if syl.visible] #why does this make the loop jerk backwards?
        to_return = syls[:len(self.pos_list)]
        for syl in to_return:
            if syl.visible:
                if syl.rect.x < self.end_first_screen_part:
                    while syl.rect.x < self.end_first_screen_part:
                        syl.rect.x += self.screenw//10
                elif syl.rect.x > self.start_third_screen_part-syl.rect.w:
                    while syl.rect.x > self.start_third_screen_part-syl.rect.w:
                        syl.rect.x -= self.screenw//10

        return to_return  # (now syls should always be bigger than this cut)

    def blit_loop(self):  # why is there some trembling? especially after downsizing screen
        self.screen_copy.fill(self.gray)
        self.end_first_screen_part = (self.screenw // 10) * ((len(self.gold_syls) // self.h) + 1)
        self.start_third_screen_part = self.screenw - (self.screenw // 10) * ((len(self.lila_syls) // self.h) + 1)
        self.tript2 = self.screen_copy.subsurface(self.end_first_screen_part, 0,
                self.start_third_screen_part - self.end_first_screen_part, self.screenh)
        self.tript2.fill(self.black)
        self.screen_syls = self.get_screensyls()
        for i in range(len(self.pos_list)):
            if self.screen_syls:
                syl = self.screen_syls.pop(0)
                if syl.visible:
                    if syl.tuple in [s.tuple for s in self.woerter.code_syls]:
                        syl.rgb = self.blink(self.fps*2, syl, self.yellow)
                        syl.image = self.default_font.render(syl.name, True, tuple(syl.rgb))
                    circle_width = 1+(self.step_fps//self.fps*2)*3
                    self.screen_copy.blit(syl.image, (syl.rect.x, self.pos_list[i] + self.syl_pos_change))
                    draw.circle(self.screen_copy,syl.rgb,syl.rect.center,syl.rect.w,width=circle_width)
                    syl.rect.y = self.pos_list[i] + self.syl_pos_change
                    syl.rect_in_circle.center = syl.rect.center
            gold = self.gold_syls[:]
            gold_tuples = [syl.tuple for syl in gold]
            code_tuples = [w.tuples for w in self.woerter.code_words]

            def find_complete_syls(syl_tuples, words_tuples):
                try:
                    nxt = next(iter([set for set in words_tuples if [t for t in set if t in syl_tuples] == [t for t in set]]))
                    return nxt
                except:
                    return None

            if not self.gw or self.gw not in code_tuples:
                self.gw = find_complete_syls(gold_tuples,code_tuples)
            lil = self.lila_syls[:]
            lila_tuples = [syl.tuple for syl in lil]
            words_tuples = [word.tuples for word in self.words]
            if not self.nw or self.nw not in words_tuples:
                self.nw = find_complete_syls(lila_tuples, words_tuples)
            for j in range(i, len(lil), self.h): # making the right columns]
                syl = lil[j]
                syl.rect.x = self.screenw - ((1 + (j // self.h)) * (self.screenw // 10)) # makes a new column further to the left whenever j becomes one more time bigger than the column length
                if self.nw and syl.tuple in self.nw:
                    syl.rgb = self.blink(self.fps*2,syl,self.red, start_color=self.white)
                    syl.image = self.default_font.render(syl.name, True, tuple(syl.rgb))
                syl.rect.y = self.top + (i * ((self.screenh-self.top) // self.h))
                self.screen_copy.blit(syl.image, syl.rect)
            for k in range(i, len(gold), self.h): # making the left columns
                syl = gold[k]
                syl.rect.x = (k // self.h) * (self.screenw // 10) # starts from width 0 for words 1-8 if ln is 8
                if self.gw and syl.tuple in self.gw:
                    syl.rgb = self.blink(self.fps*2,syl,self.red, start_color=self.white)
                    syl.image = self.default_font.render(syl.name, True, tuple(syl.rgb))
                syl.rect.y = self.top + i * ((self.screenh-self.top) // self.h)
                self.screen_copy.blit(syl.image, syl.rect)
        self.syl_pos_change += int((self.screenh / 1000) * self.syl_speed_change)
        if self.syl_pos_change >= self.screenh // self.h:
            self.syl_pos_change = 0
            self.start_syls_cut_at += 1
            if self.start_syls_cut_at > len(self.syls) - 1:  # "==" doesn't work after words get deleted
                self.start_syls_cut_at = 0
        elif self.syl_pos_change <= - self.screenh // self.h:
            self.syl_pos_change = 0
            self.start_syls_cut_at -= 1
            if self.start_syls_cut_at < 1:  # "==" doesn't work after words get deleted
                self.start_syls_cut_at = len(self.syls) - 1
        self.screen_copy.blit(self.spieler.image, self.spieler.rect)
        self.screen_transfer()

    def game_over(self):
        self.screen_copy.fill(self.black)
        text = f"Gewonnen! Das nächste Code ist: {self.output_code.upper()}." if self.won else "VERLUST! Neu starten."
        text += " Drucke SPACE, um fortzufahren."
        self.blit_clickable_words(text,self.white,(self.midtop[0],self.midtop[1] + self.down * 2))
        self.wait = True


    def dauer(self):
        dauer = 5 * 60000 - time.get_ticks()
        if dauer < 0:  # or verpixelung begins
            self.game_over()
        seconds = int(dauer / 1000 % 60)
        minutes = int(dauer / 60000 % 24)
        dauer_text = f'{minutes}:{seconds}'
        dauer_img = self.default_font.render(dauer_text, True, self.white)
        self.screen_copy.blit(dauer_img, (
            self.screen_copy.get_rect().w - dauer_img.get_rect().w,
            self.screen_copy.get_rect().h - dauer_img.get_rect().h))

    def screen_transfer(self, run=True):
        if run:
            self.dauer()
        resized_screen_copy = pg.transform.smoothscale(self.screen_copy,
                                                       self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()

    def nums(self):
        self.header.fill(self.gray)
        binary_list = {}
        splitinput = self.woerter.input_code.split()
        for i in range(len(splitinput)):  # the code?
            try:
                code_number_at_this_index = list(self.binary_code)[i]
            except:
                code_number_at_this_index = 0
            opposite = 0 if code_number_at_this_index == '1' else 1
            if i < len(self.guessed_code_words):
                if self.guessed_code_words[i].name == splitinput[i]:
                    binary_list[self.guessed_code_words[i].name] = f'{code_number_at_this_index} '
                else:
                    binary_list[f'{self.guessed_code_words[i].name} '] = f'{opposite} '
            else:
                binary_list[f'{i} '] = f'{opposite} '
        blit_h = self.blit_clickable_words(list(binary_list.values()), self.white, (self.screenw // 2, 0),afont=self.bigger_font)
        self.end_header = blit_h
        blit_h = self.blit_clickable_words([a for a in binary_list.keys() if a not in [str(b) for b in range(0,100)]], self.white,
                                           (self.screenw // 2, blit_h), no_buttons=False, screen=self.tript2)
        self.top = blit_h


    def check_num_buttons(self,click): # the buttons were made using coordinates starting from 0,0 in the screen given to blit_words()
        if self.buttons:
            click_rect = Rect(click[0],click[1],1,1)
            index = click_rect.collidelist([a.rect for a in self.buttons])
            if index != -1:
                self.move_word = index
            else:
                self.move_word = None




