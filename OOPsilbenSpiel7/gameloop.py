import pygame as pg
from pygame import *
from pygame.locals import *
from OOPsilbenSpiel7 import game
import random

class Gameloop(game.Game):
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()
        self.fall = True
        print([each.name for each in self.words])
        self.click = False
        self.mainloop()

    def mainloop(self):
        while True:
            self.screen_transfer() # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.fps) #ONE LOOP
            self.score -= 0.005 #quicker play wins more
            for e in event.get(): # CAN QUIT ONCE A LOOP
                if e.type == QUIT:
                    self.screen_copy.fill(self.black)
                    image_end = self.font.render("GAME OVER", False, self.white)
                    image_end_rect = image_end.get_rect()
                    image_end_rect.center = self.screen_copy.get_rect().center
                    self.screen_copy.blit(image_end, image_end_rect)
                    self.screen_transfer()
                    return self.score
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.fall = False
                    elif e.key == K_a:
                        for item in self.player.my_silben:
                            item.clicked_on = False
                        self.fall = True
                    elif e.key == K_c:
                        self.screen_copy.fill(self.black)
                        self.blit_def(f'cheating costs 3 seconds! one of the words means... {" ".join(random.choice(self.words).meaning)}',self.white,self.screen_copy.get_rect().midtop)
                        self.screen_transfer()
                        time.wait(3000)
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE: # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            else:
                if self.fall == True:
                    if self.sylscounter==0: # excluding the invisible ones using a counter
                        self.screen_copy.fill(self.black)
                        image_win = self.bigger_font.render(f'YOU WON!', False, self.white)
                        image_score = self.bigger_font.render(f'YOUR SCORE IS {round(self.score, 2)}', False, self.white)
                        image_win_rect = image_win.get_rect()
                        image_score_rect = image_score.get_rect()
                        image_win_rect.center = self.screen_copy.get_rect().center
                        image_score_rect.center = self.screen_copy.get_rect().center
                        image_score_rect.y += image_win_rect.h * 1.5
                        self.screen_copy.blit(image_win, image_win_rect)
                        self.screen_copy.blit(image_score, image_score_rect)
                        self.screen_transfer()
                        time.wait(3000)
                        exit()
                    else:
                        action = self.player.act() # PLAYER MOVES ONCE A LOOP
                        if action == 1: # from web result
                            self.fall = False
                        self.player.pick(self.syls)
                        self.blit_loop()
                else:
                    if self.click: # scale the mouseclick coordinates back to the original screen size
                        current_x, current_y = self.click
                        orig_screenw, orig_screenh = self.screenw, self.screenh
                        current_screenw, current_screenh = self.screen_via_display_set_mode.get_rect().size
                        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh
                        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh
                        self.click = (x,y)
                    self.desk(self.click)
                    self.click = False
