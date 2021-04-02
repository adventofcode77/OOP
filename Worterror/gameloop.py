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
                        if self.info.move_word:
                            print("move this word in gameloop:",self.info.move_word)
                            if self.info.move_word > 0:
                                self.info.guessed_code_words.insert(self.info.move_word,self.info.guessed_code_words.pop(self.info.move_word-1))
                                self.info.move_word -= 1
                            else:
                                self.info.guessed_code_words.insert(len(self.info.guessed_code_words)-1,self.info.guessed_code_words.pop(0))
                                self.info.move_word = len(self.info.guessed_code_words)-1
                        else:
                            self.info.next_counter -= 1
                            self.info.test_next_counter -= 1
                    elif e.key == K_RIGHT: # show next code_string explanation installment
                        if self.info.move_word:
                            self.info.move_word -= 1
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
                    self.click = self.scale_click(self.click,self.info.screen_copy,self.info.screen_via_display_set_mode)
                self.info.desk(self.click)
                self.click = False

    def scale_click(self, click, orig_screen, current_screen): # corr and via
        current_x, current_y = click # clicked on via
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h # the cut x,y
        current_screenw, current_screenh = current_screen.get_rect().size # the via x,y
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh # where in via x,y were
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh # where in corr they are
        return (x,y)


