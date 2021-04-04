import pygame as pg
from pygame import *
from pygame.locals import *
import random

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
        index = self.rect.collidelist([a.rect for a in sylobjects])
        if index is not -1:
            picked = sylobjects[index]
            if picked.visible:
                if self.info.tript2.get_rect().w >= self.info.screenw//10:
                    self.my_silben.append(picked)
                    if picked in self.info.woerter.code_syls:
                        self.info.gold_syls.append(picked)
                    else:
                        self.info.lila_syls.append(picked)
                picked.visible = False

    def new_start(self):
        self.info.game_over(died=True)
        self.info.next_counter = 0
        self.main_loop = True
        for item in self.info.spieler.my_silben:
            item.clicked_on = False
        self.info.gold_syls = []
        self.info.lila_syls = []
        self.info.woerter.silben, self.info.woerter.code_syls = self.info.silben_copy, self.info.code_silben_copy
        self.deleted_word_bool = False
        self.deleted_code_word_bool = False
        self.deletedlist = []
        self.deleted_word = ""
        self.start_syls_cut_at = 0
        self.pos_list = self.info.get_pos_list()
        self.info.end_first_screen_part = (self.info.screenw // 10) * ((len(self.info.gold_syls) // 10) + 1)
        self.info.start_third_screen_part = self.info.screenw - (self.info.screenw // 10) * (
                    len(self.info.lila_syls) // 10 + 1)
        self.tript2 = self.info.screen_copy.subsurface(self.info.end_first_screen_part, self.info.down,
                                                       self.info.start_third_screen_part - self.info.end_first_screen_part,
                                                       self.info.screenh - self.info.down)
        for syl in self.my_silben:
            syl.visible = True
            syl.rect.x = random.randrange(self.info.right, self.info.screenw - self.rect.w - self.info.right,
                                          self.info.screenw // 15)
        self.my_silben = []
        self.appendlist = []

