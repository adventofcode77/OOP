import pygame as pg

class Settings:
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.zuff = (200,200,200)
        self.lila = (125,33,200)
        self.fps = 60
        self.screenw, self.screenh = 500,500
        self.right = self.screenw//6
        self.down = self.screenh//12
        self.font = pg.font.SysFont("Arial",20)
        self.bigfont = pg.font.SysFont("Arial", 0)
