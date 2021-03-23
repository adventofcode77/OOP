import pygame as pg
from pygame import *
from pygame.locals import *

class Spieler():
    def __init__(self,game_instance):
        self.info = game_instance
        self.rect = pg.Rect(self.info.screenw//2,self.info.screenh//2,self.info.screen_surface//10,self.info.screen_surface//10)
        self.my_silben = []
        self.image = transform.scale(image.load('Roboter.png'),(self.rect.w,self.rect.h))
        self.speed = round(self.info.initial_syl_speed_change*1.5,2) # currently depends on fps too
        self.initial_speed = self.speed
        self.appendlist = []
        self.loop_down = True

    def act(self):
        keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x = 0 if self.speed > self.rect.x else self.rect.x - self.speed
        elif keys[K_RIGHT] or keys[K_d]:
            self.rect.right = self.info.screenw if self.rect.right + self.speed > self.info.screenw else self.rect.right + self.speed
        elif keys[K_UP] or keys[K_w]:
            self.rect.top = 0 if self.rect.top - self.speed < 0 else self.rect.top - self.speed
        elif keys[K_DOWN] or keys[K_s]:
            self.rect.bottom = self.info.screenh if self.rect.bottom + self.speed > self.info.screenh else self.rect.bottom + self.speed
        elif keys[K_0]:
            for syl in self.my_silben:
                syl.visible = True
            self.my_silben = []
            self.appendlist = []
        # change speed of itself (changes speed/direction of the loop too)
        if self.loop_down:
            if keys[K_EQUALS] or keys[K_2]:
                self.speed = round(1.1 * self.speed,2) if self.speed <= self.initial_speed * 3 else self.speed
                self.info.syl_speed_change = round(1.1 * self.info.syl_speed_change,2) if self.info.syl_speed_change <= self.info.initial_syl_speed_change * 3 else self.info.syl_speed_change
            elif keys[K_MINUS] or keys[K_1]:
                self.speed = round(0.9 * self.speed,2)
                self.info.syl_speed_change = round(0.9 * self.info.syl_speed_change,2) if self.info.syl_speed_change >= self.info.initial_syl_speed_change * 0.05 else self.info.syl_speed_change
                if self.speed <= self.initial_speed*0.05 or self.info.syl_speed_change <= self.info.initial_syl_speed_change * 0.05:
                    self.loop_down = False
                    self.info.syl_speed_change = -self.info.syl_speed_change
        else:
            if keys[K_MINUS] or keys[K_1]:
                self.speed = round(1.1 * self.speed,2) if self.speed <= self.initial_speed * 3 else self.speed
                self.info.syl_speed_change = round(1.1 * self.info.syl_speed_change,2) if self.info.syl_speed_change >= -self.info.initial_syl_speed_change * 3 else self.info.syl_speed_change
            elif keys[K_EQUALS] or keys[K_2]:
                self.speed = round(0.9 * self.speed,2)
                self.info.syl_speed_change = round(0.9 * self.info.syl_speed_change,2) if self.info.syl_speed_change <= -self.info.initial_syl_speed_change * 0.05 else self.info.syl_speed_change
                if self.speed <= self.initial_speed*0.05 or self.info.syl_speed_change >= -self.info.initial_syl_speed_change * 0.05:
                    self.loop_down = True
                    self.info.syl_speed_change = -self.info.syl_speed_change

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



