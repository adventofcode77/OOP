import pygame as pg
import math as m
from pygame import *
import math

class Settings:
    def __init__(self):
        self.screen_via_display_set_mode = pg.display.set_mode((960, 540), RESIZABLE)
        self.screen_copy = self.screen_via_display_set_mode.copy()
        # how is making a copy different than making a second screen (which didn't work)
        self.screenw, self.screenh = self.screen_copy.get_rect().size
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
        self.fps = 30
        self.font = font.SysFont("Arial",self.screen_surface//20)
        self.bigger_font = font.SysFont("Arial", self.screen_surface // 10)
        self.smaller_font = font.SysFont("Arial", self.screen_surface // 25)
        self.invisible = self.font.render("o", False, self.black)


    def get_bits(self, string, num_parts):
        definition = string
        list_of_lists = [] # list of strings?
        num_syls = num_parts if num_parts > 0 else 1
        advancement = m.ceil(len(definition)/num_syls)
        if advancement == 0:
            advancement = 1
        while definition:
            list_of_lists.append(definition[:advancement])
            definition = definition[advancement:]
        return list_of_lists # DO NOT FORGET RETURN

pg.init()
setobj = Settings()

