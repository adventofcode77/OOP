# -*- coding: utf-8 -*-
import pygame as pg
from pygame import *
from pygame.locals import *


class Spieler():
    '''
    Diese Klasse erzeugt der Spieler-Objekt mit den Methoden
     "act" (sich bewegen und seine Geschwindigkeit aendern)
     und "pick" (Silbe-Objekte aus dem Schirm sammeln)
    '''
    def __init__(self, game_instance):
        self.info = game_instance
        self.spieler_w, self.spieler_h = self.info.screen_surface // 15, self.info.screen_surface // 15
        self.rect = pg.Rect(self.info.screenw // 2, self.info.screenh // 2, self.spieler_w, self.spieler_h)
        self.my_silben = []
        self.image = transform.scale(image.load('Media/Roboter.png'), (self.rect.w, self.rect.h))
        self.normal_image = self.image.copy()
        self.brighter_image = self.image.copy()
        brighten = 100
        self.brighter_image.fill((brighten, brighten, brighten), special_flags=BLEND_RGB_ADD)
        self.speed = round(self.info.initial_syl_speed_change * 1.5, 2)  # currently depends on fps too
        self.initial_speed = self.speed
        self.appendlist = [] # TODO cant unclick words clicked before resuming play
        self.loop_down = True

    def act(self, screen_rect):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x = self.info.end_first_screen_part if self.rect.x - self.speed < self.info.end_first_screen_part else self.rect.x - self.speed
        elif keys[K_RIGHT]:
            self.rect.right = self.info.start_third_screen_part if self.rect.right + self.speed > self.info.start_third_screen_part else self.rect.right + self.speed
        elif keys[K_UP]:
            self.rect.top = 0 if self.rect.top - self.speed < 0 else self.rect.top - self.speed
        elif keys[K_DOWN]:
            self.rect.bottom = screen_rect.h if self.rect.bottom + self.speed > screen_rect.h else self.rect.bottom + self.speed
        # change speed of itself (changes speed/direction of the loop too)
        '''
        Das Reste der Methode aendert die Geschwindigkeit
        '''
        if self.loop_down:
            if keys[K_w]:
                self.speed = round(1.1 * self.speed, 2) if self.speed <= self.initial_speed * 3 else self.speed
                self.info.syl_speed_change = round(1.1 * self.info.syl_speed_change,
                                                   2) if self.info.syl_speed_change <= self.info.initial_syl_speed_change * 3 else self.info.syl_speed_change
            elif keys[K_s]:
                self.speed = round(0.9 * self.speed, 2)
                self.info.syl_speed_change = round(0.9 * self.info.syl_speed_change,
                                                   2) if self.info.syl_speed_change >= self.info.initial_syl_speed_change * 0.05 else self.info.syl_speed_change
                if self.speed <= self.initial_speed * 0.05 or self.info.syl_speed_change <= self.info.initial_syl_speed_change * 0.05:
                    self.loop_down = False
                    self.info.syl_speed_change = -self.info.syl_speed_change
        else:
            if keys[K_s]:
                self.speed = round(1.1 * self.speed, 2) if self.speed <= self.initial_speed * 3 else self.speed
                self.info.syl_speed_change = round(1.1 * self.info.syl_speed_change,
                                                   2) if self.info.syl_speed_change >= -self.info.initial_syl_speed_change * 3 else self.info.syl_speed_change
            elif keys[K_w]:
                self.speed = round(0.9 * self.speed, 2)
                self.info.syl_speed_change = round(0.9 * self.info.syl_speed_change,
                                                   2) if self.info.syl_speed_change <= -self.info.initial_syl_speed_change * 0.05 else self.info.syl_speed_change
                if self.speed <= self.initial_speed * 0.05 or self.info.syl_speed_change >= -self.info.initial_syl_speed_change * 0.05:
                    self.loop_down = True
                    self.info.syl_speed_change = -self.info.syl_speed_change

    def pick(self, visible_syls):
        index_circle_rect = self.rect.collidelist([syl.rect_in_circle for syl in visible_syls])  # collision with circle
        if index_circle_rect is not -1:
            self.image = self.brighter_image
        else:
            self.image = self.normal_image
        index_txt_rect = self.rect.collidelist([a.rect for a in visible_syls])  # collision with syl text
        if index_txt_rect is not -1:
            pikd = visible_syls[index_txt_rect]
            pikd.new_spot_rect = pikd.rect
            pikd.ghost_rect = pikd.rect_copy
            pikd.picked = self.info.fps
            self.my_silben.append(pikd)
            pikd.visible = False  # works through the variable.
            if pikd in self.info.woerter.code_syls:
                self.info.gold_syls.append(pikd)
                self.info.gute_silbe_sound.play()
                # time.wait(int(self.info.gute_silbe_sound.get_length()))
            else:
                self.info.lila_syls.append(pikd)
                self.info.bad_silbe_sound.play()
                # time.wait(int(self.info.gute_silbe_sound.get_length()))
