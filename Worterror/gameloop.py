import pygame as pg
from pygame import *
from pygame.locals import *
import random
import main

class Gameloop():
    def __init__(self, game_instance):
        self.info = game_instance
        self.clock = pg.time.Clock()  # speed depends on cpu
        self.main_loop = False
        self.menu = True
        #self.next_counter = 0
        self.click = False
        self.binary_click = False
        self.mainloop() # call last

    def mainloop(self):
        while True:
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # one loop
            for e in event.get():  # how to clear events?
                if e.type == QUIT:
                    self.info.game_over()
                elif e.type == KEYDOWN: # enum instead of if/else? dict with states and functions
                    ln = len(self.info.guessed_code_words)
                    if e.key == K_SPACE: # go to the desk
                        if self.main_loop:
                            self.main_loop = False
                        else:
                            self.menu = False
                            self.info.next_counter = 0
                            self.main_loop = True
                            for item in self.info.player.my_silben:
                                item.clicked_on = False
                    elif e.key == K_LEFT: # show next code_string explanation installment
                        if self.info.move_word is not None:
                            if self.info.move_word > 0 and self.info.move_word < ln:
                                popped = self.info.guessed_code_words.pop(self.info.move_word-1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(self.info.move_word,popped)
                                self.info.move_word -= 1
                            elif self.info.move_word == 0:
                                popped = self.info.guessed_code_words.pop(0)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(ln-1,popped)
                                self.info.move_word = len(self.info.guessed_code_words)-1
                            else:
                                print("clicked on word whose index was more than the collected code words")
                        else:
                            self.info.next_counter -= 1
                            self.info.test_next_counter -= 1
                    elif e.key == K_RIGHT: # show next code_string explanation installment
                        if self.info.move_word is not None:
                            if self.info.move_word < ln-1:
                                popped = self.info.guessed_code_words.pop(self.info.move_word + 1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(self.info.move_word, popped)
                                self.info.move_word += 1
                            elif self.info.move_word == ln-1:
                                popped = self.info.guessed_code_words.pop(ln - 1)
                                popped.color = self.info.orange
                                self.info.guessed_code_words.insert(0, popped)
                                self.info.move_word = 0
                            else:
                                print("...")
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
            elif self.main_loop:

                self.info.player.act()  # PLAYER MOVES ONCE A LOOP
                self.info.player.pick(self.info.syls)
                self.info.blit_loop()
            else:

                if self.click:  # scale the mouseclick coordinates back to the original screen size
                    self.click = self.info.scale_click(self.click,self.info.screen_copy,self.info.screen_via_display_set_mode)
                    x,y = self.click
                    print("original click",x,y)
                    x -= self.info.end_first_screen_part*2 # this offset is produced by the def of end_first_screen_part
                    self.info.check_num_buttons((x,y))
                self.info.desk(self.click)
                self.click = False




