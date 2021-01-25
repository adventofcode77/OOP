import pygame as pg
from pygame import *
import sys, time, random
from pygame.locals import *
from OOPsilbenSpiel7 import setup
from OOPsilbenSpiel7 import silbe

class Word(sprite.Sprite):
    def __init__(self, key, meaning,txtsilben):
        super().__init__()

        font = pg.font.SysFont("Arial",20)
        self.txtsilben = txtsilben
        self.name = key
        self.syls = [silbe.Silbe("it","word","def inition")] #[silbe.Silbe(a, self.name) for a in silben]
        self.meaning = meaning.split(" ")
        self.bits = self.get_bits()
        self.image = font.render(self.name,False,setup.black)
        self.rect = self.image.get_rect() # draw_rect()?
        self.rect.x = random.randrange(0,500-self.rect.w,50)
        self.speed = 3


    def get_bits(self):
        array = []
        string = self.meaning
        divisor = len(self.syls)
        for i in range(0, len(string),divisor):
            array.append([string[i:i+divisor]])
        return array
