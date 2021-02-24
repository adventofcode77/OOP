import pygame as pg
from pygame import *
from pygame.locals import *
from OOPsilbenSpiel7 import globale_variablen
import math

class Spieler():
    def __init__(self,game_instance):
        self.info = game_instance
        self.rect = pg.Rect(self.info.screenw//2,self.info.screenh//2,self.info.screen_surface//15,self.info.screen_surface//10)
        self.my_silben = []
        self.txt = self.info.font.render("player", False, self.info.black)
        self.image = transform.scale(image.load('blue_player3.svg'),(self.rect.w,self.rect.h))
        self.speed = self.info.screen_surface/20
        self.appendlist = []

    def act(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x = 0 if self.speed > self.rect.x else self.rect.x - self.speed
        elif keys[K_RIGHT]:
            self.rect.right = self.info.screenw if self.rect.right + self.speed > self.info.screenw else self.rect.right + self.speed
        elif keys[K_UP]:
            self.rect.top = 0 if self.rect.top - self.speed < 0 else self.rect.top - self.speed
        elif keys[K_DOWN]:
            self.rect.bottom = self.info.screenh if self.rect.bottom + self.speed > self.info.screenh else self.rect.bottom + self.speed
        elif keys[K_SPACE]:
            return False
        elif keys[K_2]:
            for syl in self.my_silben:
                syl.visible = True
            self.my_silben = []
            self.appendlist = []

    def pick(self,sylobjects):
        if len(self.my_silben) == 12:
            pass #print("you can only pick 12 at a time!")
        else:
            index = self.rect.collidelist([a.rect for a in sylobjects])
            if index is not -1:
                picked = sylobjects[index]
                if picked.visible == True:
                    self.my_silben.append(picked)
                    picked.visible = False



