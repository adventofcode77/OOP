# -*- coding: utf-8 -*-
class Menu:
    '''
    Diese Klasse erzeugt Die Spielanleitung
    '''
    def __init__(self, game_instance):
        self.info = game_instance

    def intro(self, schirm_zahl):
        intro_screens = {
            0: self.info.first_screen,
            1: self.info.anleitung_screen,
            -1: self.info.credits_screen
        }
        schirm_zahl = -1 if schirm_zahl > 1 or schirm_zahl < -1 else schirm_zahl
        screen_to_blit = intro_screens.get(schirm_zahl, intro_screens[0])
        self.info.screen_copy.blit(screen_to_blit, (0,0))
        return schirm_zahl
