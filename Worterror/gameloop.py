import random

import pygame as pg
from pygame import *
from pygame.locals import *


class Gameloop():
    def __init__(self, game_instance):
        self.info = game_instance
        self.clock = pg.time.Clock()  # speed depends on cpu
        self.main_loop = False
        self.menu = True
        # self.next_counter = 0
        self.click = False
        self.binary_click = False
        # self.mainloop() # call last

    def mainloop(self):
        self.info.nums()  # called here once to create self.info.top so that picked syls get painted starting from there
        while True:  # TODO: make it actually object-oriented (with classes producing the state of one object each?) +
            # advise not to use python but for example java
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # one loop
            if self.info.blink_counter:
                self.info.blink_counter += 1
            for e in event.get():  # how to clear events?
                if e.type == QUIT:
                    quit()
                elif e.type == KEYDOWN:  # enum instead of if/else? dict with states and functions
                    ln = len(self.info.guessed_code_words)
                    if e.key == K_0:
                        self.new_start()
                    elif e.key == K_5:
                        print("before", self.info.spieler.spieler_h)
                        self.info.spieler.spieler_h *= 1.1
                        self.info.spieler.spieler_w *= 1.1
                        print("after", self.info.spieler.spieler_h)
                        self.rect = pg.Rect(self.info.screenw // 2, self.info.screenh // 2, self.info.spieler.spieler_w,
                                            self.info.spieler.spieler_h)
                    elif e.key == K_4:
                        self.info.spieler.spieler_h *= 0.9
                        self.info.spieler.spieler_w *= 0.9
                        self.rect = pg.Rect(self.info.screenw // 2, self.info.screenh // 2, self.info.spieler.spieler_w,
                                            self.info.spieler.spieler_h)
                    elif e.key == K_SPACE:  # go to the desk
                        if self.info.wait:
                            if self.info.won:
                                quit()
                            self.info.wait = False
                        elif self.main_loop:
                            self.main_loop = False
                        else:
                            self.menu = False
                            self.info.next_counter = 0
                            self.main_loop = True
                            for item in self.info.spieler.my_silben:
                                item.clicked_on = False
                    elif e.key == K_LEFT:  # show next code_string explanation installment
                        if self.info.move_word is not None:
                            if self.info.move_word > 0 and self.info.move_word < ln:
                                popped = self.info.guessed_code_words.pop(self.info.move_word - 1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(self.info.move_word, popped)
                                self.info.move_word -= 1
                            elif self.info.move_word == 0:
                                popped = self.info.guessed_code_words.pop(0)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(ln - 1, popped)
                                self.info.move_word = len(self.info.guessed_code_words) - 1
                            else:
                                print("clicked on word whose index was more than the collected code words")
                        else:
                            self.info.next_counter -= 1
                            self.info.test_next_counter -= 1
                    elif e.key == K_RIGHT:  # show next code_string explanation installment
                        if self.info.move_word is not None:
                            if self.info.move_word < ln - 1:
                                popped = self.info.guessed_code_words.pop(self.info.move_word + 1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(self.info.move_word, popped)
                                self.info.move_word += 1
                            elif self.info.move_word == ln - 1:
                                popped = self.info.guessed_code_words.pop(ln - 1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(0, popped)
                                self.info.move_word = 0
                            else:
                                print("k_RIGHT + move_word > end list")
                        else:
                            self.info.next_counter += 1
                            self.info.test_next_counter += 1
                    elif e.key == K_i:
                        self.menu = True
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE:  # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            # AFTER GOING THROUGH THE EVENTS LIST
            if self.menu:
                next = self.info.menu.tutorial(self.info.next_counter, self.info.language)
                self.info.next_counter = next
            elif self.info.wait:
                self.info.game_over()
                continue
            elif self.main_loop:
                self.info.spieler.act(self.info.tript2.get_rect())  # PLAYER MOVES ONCE A LOOP
                self.info.spieler.pick([syl for syl in self.info.syls if syl.visible])
                if self.info.start_third_screen_part - self.info.end_first_screen_part < self.info.screenw // 10:
                    self.info.game_over()
                    self.new_start()
                self.info.blit_loop()
            else:
                if " ".join([word.name for word in self.info.guessed_code_words]) == self.info.woerter.input_code:
                    self.info.won = True
                    self.info.game_over()
                if self.click:  # scale the mouseclick coordinates back to the original screen size
                    self.click = self.info.scale_click(self.click, self.info.screen_copy,
                                                       self.info.screen_via_display_set_mode)
                    x, y = self.click
                    x -= self.info.end_first_screen_part  # this offset is produced by the def of end_first_screen_part
                    self.info.check_num_buttons((x, y))
                self.info.desk(self.click)
                self.click = False

    def new_start(self):
        self.info.next_counter = 0
        self.main_loop = True
        self.info.gold_syls = []
        self.info.lila_syls = []
        self.info.woerter.silben, self.info.woerter.code_syls, self.syls = self.info.silben_copy, self.info.code_silben_copy, self.info.syls_copy
        self.info.deleted_word_bool = False
        self.info.deleted_code_word_bool = False
        self.info.deletedlist = []
        self.info.deleted_word = ""
        self.info.start_syls_cut_at = 0
        self.info.pos_list = self.info.get_pos_list()
        self.info.end_first_screen_part = (self.info.screenw // 10) * ((len(self.info.gold_syls) // 10) + 1)
        self.info.start_third_screen_part = self.info.screenw - (self.info.screenw // 10) * (
                len(self.info.lila_syls) // 10 + 1)
        self.info.tript2 = self.info.screen_copy.subsurface(self.info.end_first_screen_part, self.info.down,
                                                            self.info.start_third_screen_part - self.info.end_first_screen_part,
                                                            self.info.screenh - self.info.down)

        self.info.spieler.appendlist = []
        self.info.spieler.speed = round(self.info.initial_syl_speed_change * 1.5, 2)
        self.info.spieler.loop_down = True
        for syl in self.info.spieler.my_silben:  # somehow need this despite restoring the copies
            syl.clicked_on = False
            syl.visible = True
            syl.rect.x = random.randrange(self.info.right, self.info.screenw - syl.rect.w - self.info.right,
                                          self.info.screenw // 10)
        self.info.spieler.my_silben = []
