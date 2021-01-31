import pygame as pg
import math

class Settings:
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.zuff = (200,200,200)
        self.gold = (212,175,55)
        self.lila = (125,33,200)
        self.fps = 30
        self.screenw, self.screenh = 500,500
        self.right = self.screenw//6
        self.down = self.screenh//12
        self.font = pg.font.SysFont("Arial",20)
        self.bigfont = pg.font.SysFont("Arial", 30)

    def get_bits(self,string,length):
        definition = string
        list_of_lists = []
        num_syls = length if length>0 else 1
        advancement = math.ceil(len(definition)/num_syls)
        if advancement == 0:
            advancement = 1
        while definition:
            list_of_lists.append(definition[:advancement])
            definition = definition[advancement:]
        return list_of_lists # DO NOT FORGET RETURN
