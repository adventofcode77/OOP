
import random

import pygame as pg
from pygame import *
import math


class Settings:  # there could be a function converting size/location numbers based on screen size
    def __init__(self):
        self.top = 0
        self.screen_via_display_set_mode = pg.display.set_mode((960, 540), RESIZABLE | DOUBLEBUF)
        self.screen_copy = self.screen_via_display_set_mode.copy()
        self.screen_copy = pg.transform.scale(self.screen_copy, (1920, 1080))
        self.screenw, self.screenh = self.screen_copy.get_rect().size
        self.midtop = self.screen_copy.get_rect().midtop
        self.screen_surface = int(math.sqrt(self.screenw * self.screenh))
        self.right = self.screenw // 6
        self.down = self.screenh // 12
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.zuff = (200, 255, 200)
        self.gray = (50, 50, 50)
        self.gold = (212, 175, 55)
        self.lila = (125, 33, 200)
        self.lime = (0, 255, 0)
        self.cyan = (0, 255, 255)
        self.yellow = (255, 255, 0)
        self.orange = (255, 165, 0)
        self.purple = (255, 0, 255)
        self.green = (0, 205, 0)
        self.red = (255, 0, 0)
        self.fps = 45  # keine konstante geschwindigkeit
        self.default_font = font.SysFont(None, self.screen_surface // 20)  # make one rendering function? # try excepts
        self.default_space_w = self.default_font.render(" ", True, (0, 0, 0)).get_rect().w
        self.bigger_font = font.SysFont(None, self.screen_surface // 15)
        self.smaller_font = font.SysFont(None, self.screen_surface // 30)
        self.tiny_font = font.SysFont(None, self.screen_surface // 45)
        self.space = self.font_spacing(self.default_font)
        self.invisible = self.default_font.render("o", False, self.black)
        # self.dauer_img = self.smaller_font.render(f'{5}:{0}',True,self.white)

    def font_spacing(self, font):
        img = font.render("A|&%)<QY", True, self.black)
        return img.get_rect().h

    def get_bits(self, alist, num_parts):  # goal: divide a list into roughly equal parts such that no part is empty
        list_of_lists = []
        while len(alist) < num_parts:
            alist += ["..."]
        advancement = (len(alist) // num_parts)
        if advancement == 0:
            advancement = 1
        while alist:
            if len(alist) < advancement or len(list_of_lists) >= num_parts - 1:
                list_of_lists.append(alist)
                alist = []
            else:
                list_of_lists.append(alist[:advancement])
                alist = alist[advancement:]
        if len(list_of_lists) > num_parts:
            print("get_bits() outputs more list parts than the parameter specifies")
            quit()
        return list_of_lists  # DO NOT FORGET RETURN

    def scale_click(self, click, orig_screen, current_screen):
        current_x, current_y = click
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h
        current_screenw, current_screenh = current_screen.get_rect().size
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh
        return (x, y)

    def make_rgb(self):  # hues, each for all in a word
        hue = random.choice((0, 1, 2))
        rgb = [random.randint(0, 200), random.randint(0, 200), random.randint(100, 200)]
        rgb[hue] = 255 if hue != 2 else 200
        return rgb

    def screen_transfer(self, run=True):
        if run:
            self.dauer()  # should be in screen_transfer() in order to appear in every frame
        resized_screen_copy = pg.transform.smoothscale(self.screen_copy,
                                                       self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()

    def dauer(self):
        dauer = 5 * 60000 - time.get_ticks()
        seconds = int(dauer / 1000 % 60)
        minutes = int(dauer / 60000 % 24)
        dauer_text = f'{minutes}:{seconds}'
        dauer_img = self.default_font.render(dauer_text, True, self.white)
        self.screen_copy.blit(dauer_img, (
            self.screen_copy.get_rect().w - dauer_img.get_rect().w,
            self.screen_copy.get_rect().h - dauer_img.get_rect().h))
        return dauer
