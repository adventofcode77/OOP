import random
import pygame, math

class Silbe(): #do with sprites
    silbe_all_syls = []
    def __init__(self,it,word,bit,order,worder, info, rgb): #or make it inherit from word
        self.info = info
        self.order = order
        self.name = it
        self.word = word
        self.rgb = rgb
        self.image = self.info.default_font.render(self.name, True, tuple(rgb))
        self.rect = self.image.get_rect() # or text.get_rect()?
        self.rect.x = random.randrange(self.info.right,self.info.screenw-self.rect.w-self.info.right,self.info.screenw//10)
        radius = self.rect.w
        circle_rect_side = math.sqrt(2) * radius # formula for the largest square that can fit in a circle
        self.rect_in_circle = pygame.Rect(self.rect.centerx-circle_rect_side//2,self.rect.centery-circle_rect_side,circle_rect_side,circle_rect_side)
        self.clicked_on = False
        self.bit = bit # ['einer', 'Aktiengesellschaft']
        self.visible = True
        self.tuple = (order,worder)
        Silbe.silbe_all_syls.append(self)













