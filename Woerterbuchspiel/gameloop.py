import pygame as pg
from pygame import *
from pygame.locals import *

from Woerterbuchspiel import game


class Gameloop():
    def __init__(self, input_codes, file_paths, binary_code,dict):
        self.wait, self.lost, self.won, self.new_game = False, False, False, False
        self.spielwoerter = dict
        self.input_codes = input_codes
        self.file_paths = file_paths
        self.binary_code = binary_code
        self.info = game.Game(self.input_codes, self.file_paths, self.binary_code, dict)
        self.main_loop = False
        self.menu = True
        self.click = False
        self.binary_click = False

        self.clock = pg.time.Clock()  # speed depends on cpu


    def mainloop(self):
        self.info.ziffern_und_code_woerter()  # called here once to create self.info.top so that picked syls get painted starting from there
        while True:  # TODO: make more object-oriented (with classes producing the state of one object each?)
            time_left = self.info.dauer()
            if time_left < 0:
                self.lost = True
                self.wait = True # warten, bis der Spieler Space druckt
            self.info.screen_transfer()  # resizes the last iteration's image to the current screen size and draws it
            self.clock.tick(self.info.fps)  # one loop
            if self.info.blink_counter:
                self.info.blink_counter += 1
            # EVENT LOOP
            for e in event.get():  # how to clear events?
                if e.type == QUIT:
                    quit()
                elif e.type == KEYDOWN:  # enum instead of if/else? dict with states and functions
                    ln = len(self.info.guessed_code_words)
                    if e.key == K_0:
                        self.new_start()
                    elif e.key == K_SPACE:  # go to the desk
                        print("space")
                        print("wait is",self.wait)
                        if self.wait:
                            if self.won or self.lost:
                                quit()
                            elif self.new_game:
                                self.new_start()
                            self.wait = False
                        elif self.main_loop:
                            self.main_loop = False
                        else:
                            self.menu = False
                            self.info.next_counter = 0
                            self.main_loop = True
                            for item in self.info.spieler.my_silben:
                                item.clicked_on = False
                    elif e.key == K_LEFT or e.key == K_RIGHT:  # show next code_string explanation installment
                        self.move_things_left_and_right(ln, e.key)
                    elif e.key == K_i:
                        self.menu = True
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE:  # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            # AFTER GOING THROUGH THE EVENTS LIST
            # AFTER A NEW GAME HAS STARTED
            if self.wait:
                text = f"Gewonnen! Dein Code ist: {self.info.output_code.upper()}." if self.won \
                    else "VERLOREN!" if self.lost else "NEU STARTEN!"
                text += " Drucke SPACE, um fortzufahren."
                self.info.game_over(text)
                continue
            # BEFORE THE GAMELOOP HAS STARTED
            elif self.menu:
                next = self.info.menu.tutorial(self.info.next_counter)
                self.info.next_counter = next
            elif self.main_loop:
                self.info.spieler.act(self.info.tript2.get_rect())  # PLAYER MOVES ONCE A LOOP
                self.info.spieler.pick([syl for syl in self.info.syls if syl.visible])
                # CHECKING FOR ENOUGH SPACE ON THE SCREEN
                if self.info.start_third_screen_part - self.info.end_first_screen_part < self.info.screenw // 10:
                    self.wait = True # without self.wait, the loop doesn't lead to game_over
                    self.new_game = True
                self.info.blit_loop()
            else: #
                if self.click:  # scale the mouseclick coordinates back to the original screen size
                    click_in_header = self.info.scale_click(self.click, self.info.screen_copy, self.info.header)
                    self.info.check_num_buttons(click_in_header)
                    self.click = self.info.scale_click(self.click, self.info.screen_copy,
                                                       self.info.screen_via_display_set_mode)
                    x, y = self.click
                    x -= self.info.end_first_screen_part  # this offset is produced by the def of end_first_screen_part
                    self.info.check_num_buttons((x, y))
                self.info.desk(self.click)
                self.click = False
                # GEWINNVORAUSSETZUNG
                if " ".join([word.name for word in self.info.guessed_code_words]) == self.info.woerter.code_satz:
                    self.won = True
                    self.wait = True

    def new_start(self): # Startet das ganze Spiel von neu, aber behaltet die Spielwoerter aus dem letzten
        self.info = game.Game(self.input_codes, self.file_paths, self.binary_code, self.spielwoerter)
        self.main_loop = False
        self.menu = True
        self.click = False
        self.binary_click = False
        self.wait = True
        print("new start")


    def move_things_left_and_right(self, ln, richtung): # stellt fest was die Links und Rechts Pfeilen machen
        plusminus1 = 1 if richtung == K_RIGHT else -1 # diese Wert ist entweder 1 oder -1 abhängend davon, ob Links oder Rechts gedruckt wurde
        if self.info.word_to_move is not None: # checkt, ob der Spieler auf einem der Code_Wörter geklickt hat
            # wenn ja, checkt ob dieses Wort ausser die COde Wörter Liste verlassen würde, wenn es nach links oder rechts bewegt würde
            if self.info.word_to_move >= ln-1 and richtung == K_RIGHT:
                self.info.word_to_move = ln - 1
                insert_at = 0
            elif self.info.word_to_move <= 0 and richtung == K_LEFT:
                self.info.word_to_move = 0
                insert_at = ln-1
            else:
                insert_at = self.info.word_to_move + plusminus1
            popped = self.info.guessed_code_words.pop(self.info.word_to_move) # nimmt das geklickte Wort raus aus der Liste
            popped.color = self.info.orange
            try:
                self.info.guessed_code_words.insert(insert_at, popped) # fügt das geklickte Wort einen Platz nach links oder rechts
                self.info.word_to_move = insert_at
            except:
                print("out of bounds")
        else: # wenn es kein geklicktes Wort gibt, bewegt sich der Counter für Text-Fenster nach links oder nach rechts
            self.info.next_counter += plusminus1
            self.info.test_next_counter += plusminus1


