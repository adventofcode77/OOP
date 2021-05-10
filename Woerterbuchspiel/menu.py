class Menu:
    def __init__(self, game_instance):
        self.info = game_instance
        self.offset = 0
        self.text_pos = (self.info.midtop[0], self.info.midtop[1] + self.offset + self.info.space)
        # keys
        self.move = "AWDS / LEFT RIGHT UP DOWN"
        self.pause = "SPACE"
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
        start = f"Willkommen zur Spielanleitung! Drücke {self.next} um fortzufahren oder {self.back} um zurückzugehen. " \
                f"Um die Anleitung zu SKIPPEN, drücke {self.main_loop}. "
        move = f"Um dich zu bewegen, nutze die {self.move} Tasten. Um schneller oder langsamer zu werden, " \
               f"nutze {self.accelerate} oder {self.decelerate}. " \
               f"Um die Schirmgröße anzupassen, bewege die Schirmenden. "
        goal = f"Um den Code zu bekommen, musst du Silben sammeln und einen Satz erstellen. " \
               f"Pausiere das Spiel mit {self.pause}, um klicken zu können. " \
               f"Die richtige Silben sind GELB und erscheinen LINKS. Klicke auf sie mit dem Maus. " \
               f"Die fertige Wörter erscheinen unter den Ziffern. Bewege sie mit {self.next} und {self.back}."
        game_window = f"Um diese Anleitung nochmals zu sehen, druecke {self.instructions}. " \
                      f"Drücke {self.main_loop} um zurück zum Spiel zu gehen. " \
                      f"Um fortzufahren, drücke jetzt {self.main_loop}. "
        list_de = [start, move, goal, game_window]
        return list_de
