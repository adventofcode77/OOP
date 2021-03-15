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
        self.verify_code = False
        self.menu = True
        #self.next_counter = 0
        self.click = False
        self.win_first_click = False
        self.win_second_click = False
        self.resized_copied_surface = self.info.screen_copy.copy()
        self.lang_choice = None
        self.no_language_chosen = True
        self.mainloop() # call last

    def mainloop(self):
        while True:
            self.info.score -= 0.005
            for e in event.get():  # how to clear events?
                if e.type == QUIT:
                    self.info.screen_copy.fill(self.info.black)
                    image_end = self.info.default_font.render("GAME OVER", False, self.info.white)
                    image_end_rect = image_end.get_rect()
                    image_end_rect.center = self.info.screen_copy.get_rect().center
                    self.info.screen_copy.blit(image_end, image_end_rect)
                    self.info.screen_transfer()
                    time.delay(500)
                    return self.info.score
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE: # go to the desk
                        self.main_loop = False
                    elif e.key == K_c: # see a random definition
                        self.info.screen_copy.fill(self.info.black)
                        if self.info.words:
                            tolist = f'cheating costs 5 seconds! one of the words means... {" ".join(random.choice(self.info.words).meaning)}'.split()
                            self.info.blit_string_words(tolist, self.info.white,
                                                        self.info.screen_copy.get_rect().midtop)
                        elif self.info.woerter.code_words:
                            n = random.randint(0,len(self.info.woerter.code_words)-1)
                            self.info.blit_string_words(f'cheating costs 5 seconds! The {n} code word\'s instruction bit is...'
                                                       f'{" ".join(self.info.woerter.code_words[n].meaning)}'.split(), self.info.white,
                                                        self.info.screen_copy.get_rect().midtop)
                        else:
                            self.info.blit_string_words(f'cheating costs 5 seconds! Put the words in the right order'.split(), self.info.white,
                                                        self.info.screen_copy.get_rect().midtop)
                        self.info.screen_transfer()
                        time.delay(5000)
                    elif e.key == K_v: # open win screen
                        self.verify_code = True
                    elif e.key == K_LEFT: # show next code_string explanation installment
                        print("info next counter before",self.info.test_next_counter)
                        self.info.next_counter -= 1
                        self.info.test_next_counter -= 1
                        print("info next counter after",self.info.test_next_counter)
                    elif e.key == K_RIGHT: # show next code_string explanation installment
                        print("info next counter before",self.info.test_next_counter)
                        self.info.next_counter += 1
                        self.info.test_next_counter += 1
                        print("info next counter after ",self.info.test_next_counter)
                    elif e.key == K_s:
                        self.menu = False
                        self.verify_code = False
                        self.info.next_counter = 0
                        self.main_loop = True
                        for item in self.info.player.my_silben:
                            item.clicked_on = False
                    elif e.key == K_i:
                        self.menu = True
                elif e.type == MOUSEBUTTONDOWN:
                    if self.verify_code:
                        if self.win_first_click:
                            self.win_second_click = mouse.get_pos()
                        else:
                            self.win_first_click = mouse.get_pos()
                    else:
                        self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE:  # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            # AFTER GOING THROUGH THE EVENTS LIST
            else:
                if self.menu:
                    if self.info.language:
                        self.no_language_chosen = False
                        next = self.info.menu.tutorial(self.info.next_counter, self.info.language)
                        self.info.next_counter = next
                    else:
                        self.info.menu.choose_language()
                # GUESSED WORDS WINDOW
                elif self.verify_code and self.info.guessed_code_words:
                    self.info.screen_copy.fill(self.info.black)
                    height_of_all = 0
                    len_code_words = len(self.info.guessed_code_words)
                    rects_code_words = []
                    int_rect = self.info.default_font.render('99 ', False, self.info.white).get_rect()
                    spacing = int_rect.h
                    for i in range(len_code_words): # make a visual list of rects for the positions
                        num_image = self.info.default_font.render(f'{i}', False, self.info.white)
                        num_rect = num_image.get_rect()
                        num_rect.x, num_rect.y = self.info.right + i*int_rect.w, self.info.down
                        rects_code_words.append(num_rect)
                        self.info.screen_copy.blit(num_image,num_rect) # on large_surface it's at 2000+...
                    height_of_all += self.info.down + int_rect.h + spacing
                    # PROMPT USER TO CHANGE THEIR ORDER
                    blit_h = self.info.blit_string_words(f'To change the order of the code words, click on the position'
                                                       f'of a word, then click on its new position. Use the key v to verify your choice.'.split()
                                                         , self.info.white, (self.info.midtop[0],height_of_all))
                    height_of_all = blit_h + spacing
                    if self.win_first_click and self.win_second_click: # need to scale them to surface_cut
                        self.win_first_click = self.scale_click(self.win_first_click,self.info.corrected_subsurface,self.info.screen_via_display_set_mode)
                        self.win_second_click = self.scale_click(self.win_second_click,self.info.corrected_subsurface,self.info.screen_via_display_set_mode)
                        first_click_rect = Rect(self.win_first_click[0]-self.info.padding,self.win_first_click[1],1,1) # the padding is taken out so it doens't need to be added to the rects
                        second_click_rect = Rect(self.win_second_click[0]-self.info.padding,self.win_second_click[1],1,1)
                        self.win_first_click = False
                        self.win_second_click = False
                        first_index = first_click_rect.collidelist(rects_code_words) #the actual rect positions have been shifted by padding, but to compensate this padding is taken out from the click x coordinate
                        second_index = second_click_rect.collidelist(rects_code_words)
                        if first_index is not -1 and second_index is not -1:
                            first_num = first_index
                            second_num = second_index
                            taken = self.info.guessed_code_words.pop(first_num)
                            self.info.guessed_code_words.insert(second_num,taken)
                    code_string = " ".join([word.name for word in self.info.guessed_code_words])
                    blit_h = self.info.blit_string_words(code_string.split(), self.info.yellow, (self.info.midtop[0], height_of_all)) # replace distance with a font sample height unit
                    height_of_all = blit_h + spacing
                    list_code_meanings = [" ".join(word.meaning) for word in self.info.guessed_code_words]
                    explanation = " ".join(list_code_meanings)
                    print("explanation",explanation)
                    blit_h = self.info.blit_string_words(explanation.split(), self.info.yellow, (self.info.midtop[0], height_of_all))
                    self.info.screen_transfer()

                # MAIN LOOP
                elif self.main_loop == True:
                    if " ".join([word.name for word in self.info.guessed_code_words]) == main.Main.codes[self.info.language-1]:
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
                        time.delay(3000)
                        return self.info.score
                    else:
                        self.info.player.act()  # PLAYER MOVES ONCE A LOOP
                        self.info.player.pick(self.info.syls)
                        self.info.blit_loop()
                # PICKED SYLS WINDOW
                else: #this broke after the subscreen changes
                    if self.click:  # scale the mouseclick coordinates back to the original screen size
                        self.click = self.scale_click(self.click,self.info.screen_copy,self.info.screen_via_display_set_mode)
                    self.info.desk(self.click)
                    self.click = False
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # ONE LOOP

    def scale_click(self, click, orig_screen, current_screen): # corr and via
        current_x, current_y = click # clicked on via
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h # the cut x,y
        current_screenw, current_screenh = current_screen.get_rect().size # the via x,y
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh # where in via x,y were
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh # where in corr they are
        return (x,y)
