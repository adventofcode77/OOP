import pygame as pg
import math as m
from pygame import *
import math
import random
import pygame.freetype

class Settings:
    def __init__(self): #
        pg.freetype.init()
        #self.gameloop_instance = gameloop.Gameloop()
        self.screen_via_display_set_mode = pg.display.set_mode((320, 180), RESIZABLE|DOUBLEBUF)
        print("right after making it",self.screen_via_display_set_mode.get_rect())
        self.screen_copy = self.screen_via_display_set_mode.copy()
        self.screen_copy = pg.transform.scale(self.screen_copy, (1920, 1080))
        # how is making a copy different than making a second screen (which didn't work)
        self.screenw, self.screenh = self.screen_copy.get_rect().size
        self.midtop = self.screen_copy.get_rect().midtop
        self.screen_surface = int(math.sqrt(self.screenw * self.screenh))
        self.right = self.screenw // 6
        self.down = self.screenh // 12
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.zuff = (200,255,200)
        self.gold = (212,175,55)
        self.lila = (125,33,200)
        self.lime = (0,255,0)
        self.cyan = (0,255,255)
        self.yellow = (255,255,0)
        self.orange = (255,165,0)
        self.purple = (255,0,255)
        self.green = (0,205,0)
        self.red = (255,0,0)
        self.fps = 30 # keine konstante geschwindigkeit
        self.default_font = font.SysFont("script", self.screen_surface // 20) # make one rendering function?
        self.bigger_font = font.SysFont("script", self.screen_surface // 10)
        self.smaller_font = font.SysFont("script", self.screen_surface // 30)
        self.tiny_font = font.SysFont("script", self.screen_surface // 45)
        self.space = self.font_spacing(self.default_font)
        self.invisible = self.default_font.render("o", False, self.black)

    def font_spacing(self,font):
        img = font.render("A|&%)<QY",False,self.black)
        return img.get_rect().h

    def get_bits(self,alist, num_parts): #goal: divide a list into roughly equal parts such that no part is empty
        list_of_lists = []
        while len(alist) < num_parts:
            alist += ["..."]
        advancement = (len(alist) // num_parts)
        if advancement == 0:
            advancement = 1
        while alist:
            if len(alist) < advancement or len(list_of_lists) >= num_parts-1:
                list_of_lists.append(alist)
                alist = []
            else:
                list_of_lists.append(alist[:advancement])
                alist = alist[advancement:]
        if len(list_of_lists) > num_parts:
            print("get_bits() outputs more list parts than the parameter specifies")
            quit()
        return list_of_lists # DO NOT FORGET RETURN

    def scale_click(self, click, orig_screen, current_screen): # cut and via
        current_x, current_y = click # clicked on via
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h # the cut x,y
        current_screenw, current_screenh = current_screen.get_rect().size # the via x,y
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh # where in via x,y were
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh # where in cut they are
        return (x,y)

    def make_rgb(self): # make three main hues, each for all in a word
        hue = random.choice((0,1,2))
        rgb = [random.randint(0,255),random.randint(0,255),random.randint(0,200)]
        rgb[hue] = 255
        return rgb

pg.init()
setobj = Settings()

