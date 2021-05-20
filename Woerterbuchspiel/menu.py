class Menu:
    '''
    Diese Klasse erzeugt Die Spielanleitung
    '''
    def __init__(self, game_instance):
        self.info = game_instance
        self.offset = 0
        self.text_pos = (self.info.midtop[0], self.info.midtop[1] + self.offset + self.info.space)
        # keys
        self.move = "LEFT RIGHT UP DOWN"
        self.pause = "SPACE"
        self.main_loop = "SPACE"
        self.drop_objects = 0
        self.next, self.back = "RECHTS", "LINKS"
        self.accelerate, self.decelerate = "F", "D"
        self.instructions = "I"
        self.list_instructions = self.list_lists_instructions()

    def tutorial(self, next_counter):
        '''
        Hier wird die Anleitung auf dem Schirm platziert
        :param next_counter: der aus der Liste von Anleitung-Elementen (self.list_instructions)
        :return: der Counter-Index
        '''
        self.info.screen_copy.fill(self.info.black)
        if next_counter > len(self.list_instructions) - 1:
            next_counter = 0
        elif next_counter < 0:
            next_counter = len(self.list_instructions) - 1
        blit_h = self.info.blit_clickable_words(self.list_instructions[next_counter], self.info.white,
                                                (self.info.midtop[0],
                                                 self.info.midtop[1] + self.info.down * 2),
                                                afont=self.info.smaller_font)
        self.info.resize_screen()
        return next_counter

    def list_lists_instructions(self):
        start = f"Willkommen zur Spielanleitung! " \
                f"Um die Anleitung zu SKIPPEN, drücke {self.main_loop}. " \
                f"Drücke {self.next} um die naechste Seite dieser Anletiung zu lesen," \
                f" oder {self.back} um den vorherige Seite wieder aufzurufen. "
        move = f"Um dich zu bewegen, nutze die {self.move} Tasten. Um schneller oder langsamer zu werden, " \
               f"nutze {self.accelerate} oder {self.decelerate}. " \
               f"Um die Schirmgröße anzupassen, bewege die Schirmenden. " \
               f"Pausiere das Spiel mit {self.pause}, um klicken zu können. " \
                f"Um die Pause zu beenden, druecke wieder {self.pause}. " \
               f"Mit {self.pause} kannst du ausserdem die Resultate von deinen bisherigen Mausclicks aktualisieren. " \
               f"{self.pause} bietet allerlei Moeglichkeiten! "
        goal = f"Dein Ziel ist, den naechsten Code zu finden. Er ist in Form eines Saetzes. " \
                f"Um den Code zu bekommen, musst du Silben sammeln und mit denen " \
               f"den richtigen Satz erstellen. " \
               f"Die richtige Silben sind GELB und erscheinen LINKS. " \
               f"Die falschen Silben sind alle andere Farben. " \
               f"Sie erscheinen RECHTS und hoeren sich SCHLECHT an. Vermeide sie! " \
                f"Je mehr falsche Silben du sammelst, desto weniger platz du hast, um zu spielen." \
               f"Vorsicht: zu wenig Platz fuehrt zum Verlieren." \
                f"Klicke auf die gesammelten Silben mit dem Maus, nachdem du das Spiel pausierst. " \
                f"Indem du auf sie klickst, kannst du Woerter aufbauen. " \
                   f"Die Woerter aus falschen Silben verschwinden und schaffen mehr Platz zum Spieler. " \
               f"Die Wörter den richtigen gelben Silben erscheinen unter den Ziffern. " \
                   f"Bewege sie mit {self.next} und {self.back}, um den Satz zu fertigen. "
        game_window = f"Um diese Anleitung nochmals zu sehen, druecke {self.instructions}. " \
                      f"Drücke {self.main_loop} um zurück zum Spiel zu gehen. " \
                      f"Um fortzufahren, drücke jetzt {self.main_loop}. "
        list_de = [start+move, goal, game_window]
        return list_de
