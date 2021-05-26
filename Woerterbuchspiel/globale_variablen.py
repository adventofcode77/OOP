# -*- coding: utf-8 -*-
import random

import pygame as pg
from pygame import *
import math


class Settings:  # there could be a function converting size/location numbers based on screen size
    '''
    Diese Klasse bereitet allgemeine Variablen und Methoden, die in den anderen Klassen
    mithilfe von dem Game-Objekt (das diese Klasse vererbt) benutzt werden
    '''
    def __init__(self):
        self.top = 0
        self.screen_via_display_set_mode = pg.display.set_mode((1920, 1080), RESIZABLE | DOUBLEBUF)
        self.screen_copy = self.screen_via_display_set_mode.copy()
        self.screen_copy = pg.transform.scale(self.screen_copy, (1920, 1080))
        self.screen_rect = self.screen_copy.get_rect()
        self.screenw, self.screenh = self.screen_copy.get_rect().size
        self.midtop = self.screen_copy.get_rect().midtop
        self.screen_surface = int(math.sqrt(self.screenw * self.screenh))
        self.right = self.screenw // 6
        self.down = self.screenh // 12
        self.white = (255, 255, 255)
        self.zuff = (200, 255, 200)
        self.gray = (40, 60, 80)
        self.dark = (20, 30, 40)
        self.black = (10,15,20)
        self.gold = (212, 175, 55)
        self.lila = (125, 33, 200)
        self.lime = (0, 255, 0)
        self.cyan = (0, 255, 255)
        self.yellow = (255, 255, 0)
        self.orange = (255, 165, 0)
        self.purple = (255, 0, 255)
        self.green = (0, 205, 0)
        self.red = (255, 0, 0)
        self.navy = (0,0,128)
        self.fps = 45  # keine konstante geschwindigkeit
        pg.font.init()
        self.default_font = font.SysFont(None, self.screen_surface // 20)  # make one rendering function? # try excepts
        self.default_space_w = self.default_font.render(" ", True, (0, 0, 0)).get_rect().w
        self.bigger_font = font.SysFont(None, self.screen_surface // 17)
        self.smaller_font = font.SysFont(None, self.screen_surface // 30)
        self.tiny_font = font.SysFont(None, self.screen_surface // 45)
        self.space = self.font_spacing(self.default_font)
        # self.dauer_img = self.smaller_font.render(f'{5}:{0}',True,self.white)
        self.nicht_in_bewegung = True
        self.nicht_in_intro_or_outro = False
        self.start_ticks = None
        self.time_left = 10 * 60000
        # MEDIA (falls die Pfäde falsch sind, probier die Verzeichnisse aus dem Pfad rauszunehmen)
        self.hintergrund = transform.scale(image.load('Woerterbuchspiel/Media/Sternenhintergrund2.png'), (self.screenw,self.screenh)).convert()
        # why re the below intro screens 200 short?
        self.first_screen = transform.scale(image.load('Woerterbuchspiel/Media/Intro.png'), (self.screenw+200, self.screenh)).convert()
        self.credits_screen = transform.scale(image.load('Woerterbuchspiel/Media/Credits.png'),
                                            (self.screenw+200, self.screenh)).convert()
        self.anleitung_screen = transform.scale(image.load('Woerterbuchspiel/Media/Anleitung.png'),
                                            (self.screenw+200, self.screenh)).convert()
        self.last_screen = transform.scale(image.load('Woerterbuchspiel/Media/Outro.png'),
                                                (self.screenw + 200, self.screenh)).convert()
        mixer.init()
        self.gute_silbe_sound = mixer.Sound("Woerterbuchspiel/Media/gute_silbe_sound.mp3")
        self.bad_silbe_sound = mixer.Sound("Woerterbuchspiel/Media/bad_silbe_sound.mp3")
        self.help_sign_front = self.smaller_font.render("HILFE = i", True, self.red)
        self.help_sign_back = self.smaller_font.render("ZURÜCK = i", True, self.orange)
        self.signs = [self.help_sign_front, self.help_sign_back]
        self.help_sign_index = 0

    def display_help_sign(self, sign):
        self.screen_copy.blit(self.signs[sign], (0.9 * self.screenw, self.font_spacing(self.default_font)))

    def font_spacing(self, font):
        img = font.render("A|&%)<QY", True, self.dark)
        return img.get_rect().h

    def get_bits(self, alist, num_parts):  # goal: divide a list into roughly equal parts such that no part is empty
        """
        Teilt eine Liste in so viele Teilen wie num_parts.
        :param alist: die Liste
        :param num_parts: die Anzahl an Teilen
        :return: Liste mit den Teilen
        """
        list_of_lists = []
        while len(alist) < num_parts:
            alist += ["..."]
        if num_parts == 0: num_parts = 1
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
        return list_of_lists

    def make_rgb(self):  # hues, each for all in a word
        """
        erzeugt eine RGB-Farbe aus 3 zufaellige Zahlen
        :return: die Farbe
        """
        hue = random.choice((0, 1, 2))
        rgb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 200)]
        rgb[hue] = 255 if hue != 2 else 200
        return rgb

    def scale_click(self, click, orig_screen, current_screen):
        """
        Wandelt ein Mausclick auf dem Schirm-Copy in einem Click auf dem echten Schirm,
        indem die Click-koordinaten angepasst werden
        :param click: das Mausclick
        :param orig_screen: das echte Schirm
        :param current_screen: das Schirm-Copy
        :return: das angepasste Mausclick
        """
        current_x, current_y = click
        orig_screenw, orig_screenh = orig_screen.get_rect().w, orig_screen.get_rect().h
        current_screenw, current_screenh = current_screen.get_rect().size
        current_x_ratio, current_y_ratio = current_x / current_screenw, current_y / current_screenh
        x, y = current_x_ratio * orig_screenw, current_y_ratio * orig_screenh
        return (x, y)

    def resize_and_display_screen(self):
        """
        Aendert die Groesse des Schirm-Copys auf die Groesse vom echten Schirm
        und zeichnet das Schirm-Copy auf dem echten Schirm
        :return: None
        """
        # these should be in resize_screen() in order to appear in every frame
        if self.nicht_in_intro_or_outro:
            self.display_help_sign(self.help_sign_index)
        if not self.nicht_in_bewegung:
            self.time_left = self.timer()

        resized_screen_copy = pg.transform.smoothscale(self.screen_copy,
                                                       self.screen_via_display_set_mode.get_rect().size)
        self.screen_via_display_set_mode.blit(resized_screen_copy, (0, 0))
        pg.display.flip()

    def timer(self):
        """
        Hier wird die gebliebene Zeit mittels "time.get_ticks()" berechnet
        :return: die gebliebene Zeit
        """
        seconds_left = 10 * 60 + (self.start_ticks - time.get_ticks()) // 1000
        minutes = max(0, int(seconds_left // 60))
        seconds = max(0, int(seconds_left - minutes*60))
        dauer_text = f'{minutes}:{seconds}'
        dauer_img = self.default_font.render(dauer_text, True, self.white)
        dauer_rect = dauer_img.get_rect()
        dauer_rect.x = self.screen_rect.w - dauer_rect.w
        dauer_rect.y = self.screen_rect.h - dauer_rect.h
        self.screen_copy.fill(self.navy,dauer_rect)
        self.screen_copy.blit(dauer_img, dauer_rect)
        return seconds_left
