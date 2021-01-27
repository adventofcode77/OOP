import pygame as pg
from pygame import *
from pygame.locals import *
from OOPsilbenSpiel7 import globale_variablen

class Spieler(globale_variablen.Settings):
    def __init__(self):
        super().__init__()
        l, r, w, h = 200,200,40,40
        self.rect = pg.Rect(l,r,w,h)
        self.my_silben = []
        font = pg.font.SysFont("Arial",30)
        self.txt = font.render("player", False, self.black)
        self.image = transform.scale(image.load('Lacrosse_Player.svg'),(self.rect.w,self.rect.h))
        self.speed = 8
        self.word = ""
        self.selected = []
        self.syls_for_game = [] # to return to the pool


    def act(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0+self.speed:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x <= 500-self.speed-self.rect.w:
            self.rect.x += self.speed
        elif keys[K_UP] and self.rect.y >= 0+self.speed:
            self.rect.y -= self.speed
        elif keys[K_DOWN] and self.rect.y <= 500-self.speed-self.rect.w:
            self.rect.y += self.speed
        elif keys[K_SPACE]:
            return False
        elif keys[K_2]:
            for syl in self.my_silben:
                syl.visible = True
            self.my_silben = []
            self.word = ""
            self.selected = []
            print("cleared desk")

    def pick(self,sylobjects):
        #print(sylobjects)
        if len(self.my_silben) == 12:
            pass #print("you can only pick 12 at a time!")
        else:
            index = self.rect.collidelist([a.rect for a in sylobjects])
            if index is not -1:
                picked = sylobjects[index]
                if picked not in self.my_silben:
                    self.my_silben.append(picked)
                    picked.visible = False
            else:
                self.picked = None



