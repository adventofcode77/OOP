import pygame as pg
from pygame import *
from pygame.locals import *
import random
import main

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
        self.win_first_click = False
        self.win_second_click = False
        self.corrected_subsurface = self.info.screen_copy.copy()
        self.resized_copied_surface = self.info.screen_copy.copy()
        self.padding = 0
        self.mainloop() # call last

    def mainloop(self):
        while True:
            self.info.score -= 0.005  # quicker play wins more
            for e in event.get():  # CAN QUIT ONCE A LOOP
                if e.type == QUIT:
                    self.info.screen_copy.fill(self.info.black)
                    image_end = self.info.default_font.render("GAME OVER", False, self.info.white)
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
                        if self.info.words:
                            tolist = f'cheating costs 5 seconds! one of the words means... {" ".join(random.choice(self.info.words).meaning)}'.split()
                            self.info.blit_string_word_by_word(tolist, self.info.white,
                                                               self.info.screen_copy.get_rect().midtop)
                        elif self.info.woerter.code_words:
                            self.info.blit_string_word_by_word(f'cheating costs 5 seconds! one piece of the puzzle is...'
                                                       f'{" ".join(random.choice(self.info.woerter.code_words).meaning)}'.split(), self.info.white,
                                                               self.info.screen_copy.get_rect().midtop)
                        else:
                            self.info.blit_string_word_by_word(f'cheating costs 5 seconds! Put the words in the right order'.split(), self.info.white,
                                                               self.info.screen_copy.get_rect().midtop)
                        self.info.screen_transfer()
                        time.wait(5000)
                    elif e.key == K_w: # open win screen
                        self.win = True
                    elif e.key == K_e: # close win screen
                        self.win = False
                    elif e.key == K_d: # show next code_string explanation installment
                        self.next = True
                elif e.type == MOUSEBUTTONDOWN:
                    if self.win:
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
                # GUESSED WORDS WINDOW
                if self.win and self.info.guessed_code_words:
                    self.info.screen_copy.fill(self.info.black)
                    self.info.large_surface.fill(self.info.black)
                    surface_cut = pg.Surface.subsurface(self.info.large_surface,pg.Rect(2000,0,3000,3000))
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
                        surface_cut.blit(num_image,num_rect) # on large_surface it's at 2000+...
                    height_of_all += self.info.down + int_rect.h + spacing
                    # PROMPT USER TO CHANGE THEIR ORDER
                    blit_h = self.info.blit_string_word_by_word(f'To change the order of the code_string words, click on the position'
                                                       f'of a word, then click on its new position. Use the key v to verify your choice.'.split()
                                                       , self.info.white, (self.info.midtop[0],height_of_all), screen=surface_cut)
                    height_of_all = blit_h + spacing
                    if self.win_first_click and self.win_second_click: # need to scale them to surface_cut
                        self.win_first_click = self.scale_click(self.win_first_click,self.corrected_subsurface,self.info.screen_via_display_set_mode)
                        self.win_second_click = self.scale_click(self.win_second_click,self.corrected_subsurface,self.info.screen_via_display_set_mode)
                        first_click_rect = Rect(self.win_first_click[0]-self.padding,self.win_first_click[1],1,1) # the padding is taken out so it doens't need to be added to the rects
                        second_click_rect = Rect(self.win_second_click[0]-self.padding,self.win_second_click[1],1,1)
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
                    blit_h = self.info.blit_string_word_by_word(code_string.split(), self.info.yellow, (self.info.midtop[0], height_of_all),screen=surface_cut) # replace distance with a font sample height unit
                    height_of_all = blit_h + spacing
                    list_code_meanings = [word.meaning for word in self.info.guessed_code_words]
                    explanation = " ".join(list_code_meanings[self.next_counter])
                    blit_h = self.info.blit_string_word_by_word(explanation.split(),self.info.yellow,(self.info.midtop[0],height_of_all),screen=surface_cut)
                    height_of_all = blit_h + spacing
                    if self.next:
                        if self.next_counter >= len(list_code_meanings)-1:
                            self.next_counter = 0
                        else:
                            self.next_counter += 1
                        self.next = False
                    if height_of_all > self.info.screen_copy.get_rect().h:
                        orig_width,orig_height = self.info.screen_copy.get_rect().w,self.info.screen_copy.get_rect().h
                        new_height = height_of_all
                        ratio = new_height / orig_height
                        new_width = orig_width * ratio
                        self.padding = (new_width - orig_width) // 2 # indents the cut to the left so the new width can take black background proportionately from left and right
                        self.corrected_subsurface = pg.Surface.subsurface(self.info.large_surface,pg.Rect((2000 - self.padding,0,new_width,new_height)))
                        self.resized_copied_surface = pg.transform.scale(self.corrected_subsurface, (self.info.screen_copy.get_rect().w,self.info.screen_copy.get_rect().h))
                        self.info.screen_copy.blit(self.resized_copied_surface,(0,0))
                    else:
                        self.resized_copied_surface = pg.Surface.subsurface(self.info.large_surface,pg.Rect(2000,0,self.info.screen_copy.get_rect().w,self.info.screen_copy.get_rect().h))
                        self.info.screen_copy.blit(self.resized_copied_surface,(0,0))
                    self.info.screen_transfer()


                # MAIN LOOP
                elif self.fall == True:

                    print(" ".join([word.name for word in self.info.guessed_code_words]))
                    print(main.Main.code)
                    if " ".join([word.name for word in self.info.guessed_code_words]) == main.Main.code:
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
                # PICKED SYLS WINDOW
                else:
                    if self.click:  # scale the mouseclick coordinates back to the original screen size
                        current_x, current_y = self.click
                        orig_screenw, orig_screenh = self.info.screenw, self.info.screenh
                        current_screenw, current_screenh = self.info.screen_via_display_set_mode.get_rect().size
                        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh
                        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh
                        self.click = (x, y)
                    #self.info.large_surface.fill(self.info.black)
                    self.info.desk(self.click)
                    self.click = False
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # ONE LOOP

    def scale_click(self, click, orig_screen, current_screen): # cut and via
        current_x, current_y = click # clicked on via
        print("the click on via:",current_x, current_y)
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h # the cut x,y
        print("the cut w,h",orig_screenw, orig_screenh)
        current_screenw, current_screenh = current_screen.get_rect().size # the via x,y
        print("the via w,h",current_screenw, current_screenh)
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh # where in via x,y were
        print("where in via were x,y",current_x_ratio, current_y_ratio)
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh # where in cut they are
        print("where in cut are x,y",x, y)
        return (x,y)
