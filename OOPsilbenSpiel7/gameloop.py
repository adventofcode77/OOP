import pygame as pg
from pygame import *
from pygame.locals import *
from OOPsilbenSpiel7 import game

class Gameloop(game.Game):
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()
        self.run = True
        print([each.name for each in self.words])
        self.click = False
        self.mainloop()

    def mainloop(self):
        while True:
            self.screen_transfer()
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
                    #print(self.player.screenwidth,self.player.screenheight)
                    return self.score
                elif e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.run = False
                    elif e.key == K_a:
                        for item in self.player.my_silben:
                            item.clicked_on = False
                        self.run = True
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                    print(f'mouseclick at {self.click}')
                elif e.type == VIDEORESIZE:
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
                    self.screenw, self.screenh = e.size
                    print(self.screenw,self.screenh)
            else:
                if self.run == True:
                    if self.sylscounter==0: # including the invisible ones
                        self.screen_copy.fill(self.black)
                        image_win = self.bigfont.render(f'YOU WON!', False, self.white)
                        image_score = self.bigfont.render(f'YOUR SCORE IS {round(self.score, 3)}', False, self.white)
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
                            self.run = False
                        self.player.pick(self.syls)
                        self.blit_loop()
                else:
                    self.desk(self.click)
                    self.click = False
