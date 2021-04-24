class Menu:
    def __init__(self, game_instance):
        self.info = game_instance
        self.offset = 0
        self.text_pos = (self.info.midtop[0], self.info.midtop[1] + self.offset + self.info.space)
        # keys
        self.move = "AWDS / LEFT RIGHT UP DOWN"
        self.workspace_window = "SPACE"
        self.main_loop = "SPACE"
        self.drop_objects = 0
        self.next, self.back = "RECHTS", "LINKS"
        self.accelerate, self.decelerate = "PLUS / 2", "MINUS / 1"
        self.instructions = "I"
        self.list_instructions = self.list_lists_instructions()

    def tutorial(self, next_counter):
        self.info.screen_copy.fill(self.info.black)
        if next_counter > len(self.list_instructions) - 1:
            next_counter = 0
        elif next_counter < 0:
            next_counter = len(self.list_instructions) - 1
        blit_h = self.info.blit_clickable_words(self.list_instructions[next_counter], self.info.white,
                                                (self.info.midtop[0],
                                                 self.info.midtop[1] + self.info.down * 2),
                                                afont=self.info.smaller_font)
        self.info.screen_transfer()
        return next_counter

    def list_lists_instructions(self):
        start = f"Willkommen zum Spielanleitung! Drücke {self.next} um fortzufahren oder {self.back} um zurückzugehen. Um die Anleitung zu SKIPPEN, drücke {self.main_loop}. "
        move = f"Um dich zu bewegen, nutze die {self.move} Tasten. Um schneller oder langsamer zu werden, nutze {self.accelerate} oder {self.decelerate}. " \
               " Warnung: Alles auf der Schirm wird seine Geschwindigkeit aendern. "
        goal = f"Dein Ziel ist, ein Code zu finden. Der Code sieht aus wie ein Satz. " \
               f"Um den Satz zu bekommen, musst du die richtige Woerter in der richtigen Reihenfolge zusammensetzen. " \
               f"Die Woerter findest du, indem du Silben sammelst und sie ebenso zusammensetzest. Du kannst bis 12 Silben sammeln. " \
               f"Um sie zu entlasen, druecke {self.drop_objects}. "
        game_window = f"Um das Spiel zu beenden, druecke auf X. Um die Schirmgroesse anzupassen, bewege die Schirmenden. " \
                      f"Um diese Anleitung nochmals zu sehen, druecke {self.instructions}. Druecke {self.main_loop} um zurueck zum Spiel zu gehen." \
                      f"Um fortzufahren, druecke jetzt {self.main_loop}. "

        list_de = [start, goal, move, game_window]

        return list_de
