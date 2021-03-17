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
        self.verified_choice = False
        self.gewonnen = False
        self.binary_click = False
        self.list_index_binary_click_words = []
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
                        self.info.next_counter -= 1
                        self.info.test_next_counter -= 1
                    elif e.key == K_RIGHT: # show next code_string explanation installment
                        self.info.next_counter += 1
                        self.info.test_next_counter += 1
                    elif e.key == K_s:
                        self.menu = False
                        self.verify_code = False
                        self.info.next_counter = 0
                        self.main_loop = True
                        for item in self.info.player.my_silben:
                            item.clicked_on = False
                    elif e.key == K_i:
                        self.menu = True
                    elif e.key == K_y:
                        self.verified_choice = True
                elif e.type == MOUSEBUTTONDOWN:
                    if self.verify_code:
                        if self.gewonnen == True:
                            self.binary_click = mouse.get_pos()
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
                    rects_code_words = []
                    int_rect = self.info.default_font.render('99 ', False, self.info.white).get_rect()
                    spacing = int_rect.h
                    for i in range(len(self.info.woerter.input_code.split())): # the code?
                        if i < len(self.info.guessed_code_words):
                            code_number_at_this_index = list(self.info.binary_code)[i]
                            opposite = 0 if code_number_at_this_index == '1' else 1
                            if self.info.guessed_code_words[i].name == self.info.woerter.input_code.split()[i]:
                                num_image = self.info.default_font.render(f'{code_number_at_this_index}', False, self.info.white)
                            else:
                                num_image = self.info.default_font.render(f'{opposite}', False,
                                                                          self.info.white)
                        else:
                            num_image = self.info.default_font.render(f'{0 if i%2==0 else 1}', False,self.info.white)
                        num_rect = num_image.get_rect()
                        num_rect.x, num_rect.y = self.info.right + i*int_rect.w, self.info.down
                        rects_code_words.append(num_rect)
                        self.info.screen_copy.blit(num_image,num_rect) # on large_surface it's at 2000+...
                    height_of_all += self.info.down + int_rect.h + spacing
                    # PROMPT USER TO CHANGE THEIR ORDER
                    blit_h = self.info.blit_string_words(f'Druecke auf ein Wort und danach auf dem Platz, wo du es umstellen willst. '
                                                         f'Zum Bestätigen der Auswahl, druecke auf Y'.split()
                                                         , self.info.white, (self.info.midtop[0],height_of_all))
                    height_of_all = blit_h + spacing

                    clicked1, clicked2 = None, None

                    if self.win_first_click:
                        self.win_first_click = self.scale_click(self.win_first_click, self.info.screen_copy,
                                                                self.info.screen_via_display_set_mode)
                        first_click_rect = Rect(self.win_first_click[0], self.win_first_click[1], 1, 1)
                        first_index = first_click_rect.collidelist([word.rect for word in self.info.guessed_code_words])
                        if first_index != -1:
                            clicked1 = first_index
                    if self.win_second_click:
                        self.win_second_click = self.scale_click(self.win_second_click, self.info.screen_copy,
                                                                 self.info.screen_via_display_set_mode)
                        second_click_rect = Rect(self.win_second_click[0], self.win_second_click[1], 1, 1)
                        second_index = second_click_rect.collidelist(
                            [word.rect for word in self.info.guessed_code_words])
                        if second_index != -1:
                            clicked2 = second_index
                        if self.verified_choice:
                            self.verified_choice = False
                            self.win_first_click = False
                            self.win_second_click = False
                            to_move = self.info.guessed_code_words.pop(first_index)
                            self.info.guessed_code_words.insert(second_index, to_move)


                    last_line_down = height_of_all
                    screen_rect = self.info.screen_copy.get_rect()
                    last_word_right = 0.25 * screen_rect.w
                    window_counter = 0
                    font = self.info.default_font
                    copy_screen = self.info.screen_copy.copy()
                    list_snapshots_to_blit = {}
                    for i in range(len(self.info.guessed_code_words)): # combine w blit string?
                        color = self.info.green if i == clicked1 else self.info.red if  i == clicked2 else self.info.yellow if i in self.list_index_binary_click_words else self.info.cyan
                        word = self.info.guessed_code_words[i]
                        word_img = font.render(word.name + " ", False, color)
                        word_rect = word_img.get_rect()
                        if last_word_right >= 0.75 * screen_rect.w:
                            if last_line_down < screen_rect.h - spacing * 3:  # twice the highest spacing?
                                last_word_right = 0.25 * screen_rect.w
                                last_line_down += spacing
                                word_rect.x, word_rect.y = last_word_right, last_line_down
                                copy_screen.blit(word_img, word_rect)
                                last_word_right += word_rect.w
                            else:
                                copy_screen = self.info.screen_copy.copy()
                                last_line_down = height_of_all
                                last_word_right = 0.25 * copy_screen.get_rect().w
                                window_counter += 1
                                word_rect.x, word_rect.y = last_word_right, last_line_down
                                copy_screen.blit(word_img, word_rect)
                                last_word_right += word_rect.w
                        else:
                            word_rect.x, word_rect.y = last_word_right, last_line_down
                            copy_screen.blit(word_img, word_rect)
                            last_word_right += word_rect.w
                        list_snapshots_to_blit[window_counter] = copy_screen.copy()
                        word.image = word_img
                        word.rect = word_rect
                    if len(list_snapshots_to_blit) == 0:
                        list_snapshots_to_blit[window_counter] = self.info.screen_copy.copy()
                    if self.info.test_next_counter < 0:
                        temp_counter = len(list_snapshots_to_blit) - 1 - (
                                    self.info.test_next_counter % len(list_snapshots_to_blit))
                    else:
                        temp_counter = self.info.test_next_counter % len(list_snapshots_to_blit)
                    self.info.screen_copy.blit(list_snapshots_to_blit[temp_counter], (0, 0))

                    height_of_all = last_line_down + spacing
                    if not self.gewonnen:
                        list_code_meanings = [" ".join(word.meaning) for word in self.info.guessed_code_words]
                        explanation = " ".join(list_code_meanings)
                        blit_h = self.info.blit_string_words(explanation.split(), self.info.yellow, (self.info.midtop[0], height_of_all))
                    self.info.screen_transfer()

                    if " ".join([word.name for word in self.info.guessed_code_words]) == main.Main.codes[self.info.language-1]:
                        self.gewonnen = True
                        indices_ones = []
                        for i in range(len(self.info.binary_code)):
                            num = self.info.binary_code[i]
                            if num == "1":
                                indices_ones.append(i)
                        self.info.screen_copy.fill(self.info.black,Rect(0,height_of_all,self.info.screen_copy.get_rect().w,self.info.screen_copy.get_rect().h))
                        self.info.blit_string_words(f'Du hast den Code-Satz fast erhalten! Die binärische Representation'
                                                    f'zeigt die {len(indices_ones)} Schluessel-Woerter. Wähle sie aus.', self.info.gold,(self.info.midtop[0],height_of_all))
                        if self.binary_click:
                            binary_click_rect = Rect(self.binary_click[0],self.binary_click[1],1,1)
                            self.binary_click = False
                            index = binary_click_rect.collidelist(self.info.guessed_code_words)
                            if index != -1:
                                self.list_index_binary_click_words.append(index)
                        if self.list_index_binary_click_words == indices_ones:
                            self.info.screen_copy.fill(self.info.black,Rect(0,height_of_all,self.info.screen_copy.get_rect().w,self.info.screen_copy.get_rect().h))
                            self.info.blit_string_words(f'RICHTIG',self.info.gold,self.info.midtop)
                            self.info.screen_transfer()
                            time.delay(10000)
                            return self.info.score
                        self.info.screen_transfer()




                # MAIN LOOP
                elif self.main_loop == True:
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
