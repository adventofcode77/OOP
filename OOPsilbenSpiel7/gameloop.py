import pygame as pg
from pygame import *
from pygame.locals import *
from OOPsilbenSpiel7 import woerterbuch
import random
from OOPsilbenSpiel7 import game


class Gameloop():
    def __init__(self, game_instance):
        self.info = game_instance
        self.clock = pg.time.Clock()  # speed depends on cpu
        self.fall = True
        self.win = False
        self.next = False
        self.next_counter = 0
        print([each.name for each in self.info.words])
        self.click = False
        self.mainloop() # call last

    def mainloop(self):
        while True:
            self.info.score -= 0.005  # quicker play wins more
            for e in event.get():  # CAN QUIT ONCE A LOOP
                if e.type == QUIT:
                    self.info.screen_copy.fill(self.info.black)
                    image_end = self.info.font.render("GAME OVER", False, self.info.white)
                    image_end_rect = image_end.get_rect()
                    image_end_rect.center = self.info.screen_copy.get_rect().center
                    self.info.screen_copy.blit(image_end, image_end_rect)
                    self.info.screen_transfer()
                    time.wait(500)
                    return self.info.score
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE: # go to the desk
                        self.fall = False
                    elif e.key == K_a: # return from the desk
                        for item in self.info.player.my_silben:
                            item.clicked_on = False
                        self.fall = True
                    elif e.key == K_c: # see a random definition
                        self.info.screen_copy.fill(self.info.black)
                        if (self.info.words):
                            self.info.blit_string_word_by_word(f'cheating costs 5 seconds! one of the words means... '
                                                       f'{" ".join(random.choice(self.info.words).meaning)}', self.info.white,
                                                               self.info.screen_copy.get_rect().midtop)
                        else:
                            self.info.blit_string_word_by_word(f'cheating costs 5 seconds! one piece of the puzle is...'
                                                       f'{" ".join(random.choice(self.info.woerter.code_words).meaning)}', self.info.white,
                                                               self.info.screen_copy.get_rect().midtop)
                        self.info.screen_transfer()
                        time.wait(5000)
                    elif e.key == K_w: # open win screen
                        self.win = True
                    elif e.key == K_e: # close win screen
                        self.win = False
                    elif e.key == K_d: # show next code explanation installment
                        self.next = True
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE:  # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            else:
                if self.win:
                    self.info.screen_copy.fill(self.info.black)
                    code = " ".join([word.name for word in self.info.guessed_code_words])
                    self.info.blit_string_word_by_word(code, self.info.yellow, self.info.screen_copy.get_rect().midtop)
                    list_code_meanings = [word.meaning for word in self.info.guessed_code_words]
                    explanation = " ".join(list_code_meanings[self.next_counter])
                    self.info.blit_string_word_by_word(explanation,self.info.yellow,self.info.screen_copy.get_rect().center)
                    if self.next:
                        if self.next_counter >= len(list_code_meanings)-1:
                            self.next_counter = 0
                        else:
                            self.next_counter += 1
                        self.next = False
                    self.info.screen_transfer()
                elif self.fall == True:
                    if self.info.sylscounter == 0:  # excluding the invisible ones using a counter
                        self.info.screen_copy.fill(self.info.black)
                        image_win = self.info.bigger_font.render(f'YOU WON!', False, self.info.white)
                        image_score = self.info.bigger_font.render(f'YOUR SCORE IS {round(self.info.score, 2)}', False,
                                                              self.info.white)
                        image_win_rect = image_win.get_rect()
                        image_score_rect = image_score.get_rect()
                        image_win_rect.center = self.info.screen_copy.get_rect().center
                        image_score_rect.center = self.info.screen_copy.get_rect().center
                        image_score_rect.y += image_win_rect.h * 1.5
                        self.info.screen_copy.blit(image_win, image_win_rect)
                        self.info.screen_copy.blit(image_score, image_score_rect)
                        self.info.screen_transfer()
                        time.wait(3000)
                        return self.info.score
                    else:
                        action = self.info.player.act()  # PLAYER MOVES ONCE A LOOP
                        if action == 1:  # from web result
                            self.fall = False
                        self.info.player.pick(self.info.syls)
                        self.info.blit_loop()
                else:
                    if self.click:  # scale the mouseclick coordinates back to the original screen size
                        current_x, current_y = self.click
                        orig_screenw, orig_screenh = self.info.screenw, self.info.screenh
                        current_screenw, current_screenh = self.info.screen_via_display_set_mode.get_rect().size
                        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh
                        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh
                        self.click = (x, y)
                    self.info.desk(self.click)
                    self.click = False
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # ONE LOOP
