import pygame as pg
import math as m
from pygame import *
import math
import random
import main

class Settings:
    def __init__(self): #
        self.file_path = main.Main.file_path # filter unsuitable words
        #self.gameloop_instance = gameloop.Gameloop()
        self.screen_via_display_set_mode = pg.display.set_mode((960, 540), RESIZABLE|DOUBLEBUF)
        self.screen_copy = self.screen_via_display_set_mode.copy()
        self.large_surface = self.screen_via_display_set_mode.copy()
        self.large_surface = pg.transform.scale(self.large_surface,(7000,7000))
        # how is making a copy different than making a second screen (which didn't work)
        self.screenw, self.screenh = self.screen_copy.get_rect().size
        self.midtop = self.screen_copy.get_rect().midtop
        self.large_midtop = self.large_surface.get_rect().midtop
        self.screen_surface = int(math.sqrt(self.screenw * self.screenh))
        self.right = self.screenw // 6
        self.down = self.screenh // 12
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.zuff = (200,200,200)
        self.gold = (212,175,55)
        self.lila = (125,33,200)
        self.lime = (0,255,0)
        self.cyan = (0,255,255)
        self.yellow = (255,255,0)
        self.orange = (255,165,0)
        self.purple = (255,0,255)
        self.fps = 30 # keine konstante geschwindigkeit
        self.default_font = font.SysFont("Arial", self.screen_surface // 20) # make one rendering function?
        self.bigger_font = font.SysFont("Arial", self.screen_surface // 10)
        self.smaller_font = font.SysFont("Arial", self.screen_surface // 20)
        self.tiny_font = font.SysFont("Arial", self.screen_surface // 45)
        self.invisible = self.default_font.render("o", False, self.black)



    def get_bits(self, string, num_parts):
        definition = string
        #print(definition)
        list_of_lists = [] # list of strings
        num_syls = num_parts if num_parts > 0 else 1
        advancement = m.ceil(len(definition)/num_syls)
        if advancement == 0:
            advancement = 1
        while definition:
            list_of_lists.append(definition[:advancement])
            definition = definition[advancement:]
        #print("get bits listoflists",list_of_lists)
        return list_of_lists # DO NOT FORGET RETURN

    def scale_click(self, click, orig_screen, current_screen): # cut and via
        current_x, current_y = click # clicked on via
        print("the click on via:",current_x, current_y)
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h # the cut x,y
        print("the corr w,h",orig_screenw, orig_screenh)
        current_screenw, current_screenh = current_screen.get_rect().size # the via x,y
        print("the via w,h",current_screenw, current_screenh)
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh # where in via x,y were
        print("where in via were x,y",current_x_ratio, current_y_ratio)
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh # where in cut they are
        print("where in corr are x,y",x, y)
        return (x,y)

    def make_rgb(self): # make three main hues, each for all in a word
        hue = random.choice((0,1,2))
        rgb = [100,100,100]
        rgb[0],rgb[1],rgb[2] = random.randint(0,200),random.randint(0,200),random.randint(0,150)
        rgb[hue] = 255
        return rgb

pg.init()
setobj = Settings()

