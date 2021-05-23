import pygame as pg
from pygame import *
from pygame.locals import *

from Woerterbuchspiel import game


class Gameloop():
    '''
    Diese Klasse kontrolliert das Spiel.
    Wenn diese Klasse initiiert wird, erzeugt sie ein Objekt aus dem Klasse Game.
    Das Game Objekt beeinhaltet zusaetzliche Methoden und Variablen, die die Gameloop Klasse nutzt.
    '''
    def __init__(self, input_codes, file_paths, binary_code,dict):
        '''
        Hier werden Variablen definiert, die entweder True oder False sind,
        die das "State" des Spiels bestimmen.

        :param input_codes: Das Code-Satz, das die Aufgabe des Spielers ist, zu erraten
        :param file_paths: Das ganze Woerterbuch im XML Format (momentan nicht benutzt)
        :param binary_code: Das uebernommene Code aus dem letzten Spiel
        :param dict: Das momentan benutzte Woerterbuch
        '''
        self.wait, self.lost, self.won, self.new_game = False, False, False, False
        self.spielwoerter = dict
        self.input_codes = input_codes
        self.file_paths = file_paths
        self.binary_code = binary_code
        self.game_objekt = game.Game(self.input_codes, self.file_paths, self.binary_code, dict)
        self.main_loop = False
        self.menu = True
        self.click = False
        self.binary_click = False
        self.time_left = None

        self.clock = pg.time.Clock()  # speed depends on cpu?




    def mainloop(self):
        '''
        Hier laeuft das ganze Spiel vom Beginn zum Ende.
        Diese Methode besteht hauptzaechlich aus der While schleife.
        Vor der While Schleife wird die Methode ziffern_und_code_woerter()
        aus der Klasse Main aufgerufen, um Layout-Variablen zu aktualisieren.
        :return: None
        '''
        self.game_objekt.ziffern_und_code_woerter()  # called here once to create self.info.top so that picked syls get painted starting from there

        while True:  # TODO: make more object-oriented (with classes producing the state of one object each?)
            self.clock.tick(self.game_objekt.fps)  # one loop?
            self.game_objekt.resize_and_display_screen()  # resizes the last iteration's image to the current screen size and draws it
            if self.game_objekt.blink_counter:
                self.game_objekt.blink_counter += 1
            # EVENT LOOP
            '''
            In dieser FOR Schleife wird durch die Maus- und Taste- Events gegangen 
            und die Folgen von jedem bestimmt
            '''
            for e in event.get():  # how to clear events?
                '''switch e.type
                case QUIT:
                    quit();
                case KEYDOWN:
                    ..'''
                if e.type == QUIT:
                    print("closed the game window")
                    quit()
                    print("should not print")
                elif e.type == KEYDOWN:
                    ln = len(self.game_objekt.guessed_code_words)
                    if e.key == K_0:
                        self.new_start()
                    elif e.key == K_SPACE:  # go to the desk
                        if self.wait:
                            if self.won or self.lost:
                                quit()
                            elif self.new_game:
                                self.new_start()
                                self.game_objekt.ziffern_und_code_woerter()  # called here once to create self.info.top so that picked syls get painted starting from there
                            self.wait = False
                        elif self.main_loop:
                            self.main_loop = False
                        else:
                            self.menu = False
                            if not self.game_objekt.start_ticks:
                                self.game_objekt.start_ticks = time.get_ticks()
                            self.game_objekt.next_counter = 0
                            self.main_loop = True
                            # clear the list and attributes for making words so that you start anew next time
                            for item in self.game_objekt.spieler.my_silben:
                                item.clicked_on = False
                            self.game_objekt.spieler.appendlist = []
                    elif e.key == K_LEFT or e.key == K_RIGHT:  # show next code_string explanation installment
                        self.move_things_left_and_right(ln, e.key)
                    elif e.key == K_i:
                        self.menu = True
                    elif e.key == K_DOWN:
                        self.menu = False
                        if not self.game_objekt.start_ticks:
                            self.game_objekt.start_ticks = time.get_ticks()
                        self.game_objekt.next_counter = 0
                        self.main_loop = True
                        for item in self.game_objekt.spieler.my_silben:
                            item.clicked_on = False
                elif e.type == MOUSEBUTTONDOWN:
                    self.click = mouse.get_pos()
                elif e.type == VIDEORESIZE:  # updates the size to which the screen_copy image should be scaled
                    self.screen_via_display_set_mode = pg.display.set_mode(e.size, RESIZABLE)
            # AFTER GOING THROUGH THE EVENTS LIST
            # AFTER A NEW GAME HAS STARTED
            self.check_time_left(self.time_left)
            if self.wait:
                '''
                Hier ist der Zustand des Spiels entweden gewonnen, verloren oder Neustart
                '''
                if self.won:
                    self.game_objekt.screen_copy.blit(self.game_objekt.last_screen, (0,0))

                else:
                    text = "VERLOREN!" if self.lost else "NEU STARTEN!"
                    text += " Drucke SPACE, um fortzufahren."
                    self.game_objekt.game_over(text)
                continue
            # BEFORE THE GAMELOOP HAS STARTED
            elif self.menu:
                '''
                Hier ist der Zustand des Spiels entweder "am Anfang bei der Anleitung" oder
                "pausiert, um die Anleitung nochmals zu lesen"
                '''
                self.game_objekt.nicht_in_bewegung = True
                # next = self.game_objekt.menu.tutorial(self.game_objekt.next_counter)
                next = self.game_objekt.menu.intro(self.game_objekt.next_counter)
                self.game_objekt.next_counter = next
            elif self.main_loop:
                '''
                Hier ist der Zustand des Spiels "im Action-Loop".
                Der Loop besteht aus dem Spieler-Objekt und Silbe-Objekte.
                '''
                self.game_objekt.nicht_in_bewegung = False
                self.game_objekt.spieler.act(self.game_objekt.tript2.get_rect())  # PLAYER MOVES ONCE A LOOP
                self.game_objekt.spieler.pick([syl for syl in self.game_objekt.syls if syl.visible])
                # CHECKING FOR ENOUGH SPACE ON THE SCREEN
                if self.game_objekt.start_third_screen_part - self.game_objekt.end_first_screen_part < self.game_objekt.screenw // 10:
                    '''
                    Hier wird geprueft, ob der Spielplatz zu niedrig geworden sind,
                    indem die Gesammelte Silbe-Objekte zu viele Spalten genommen haben.
                    In diesem Fall wird der Neustart-Zustand mithilfe der Variable self.new_game aufgerufen.
                    '''
                    self.wait = True # without self.wait, the loop doesn't lead to game_over
                    self.new_game = True
                self.game_objekt.blit_loop()
            #  WENN LOOP PAUSIERT IST
            else:
                '''
                Hier ist der Zustand des Spiels "pausiert"
                '''
                # WENN GEKLICKT WIRD

                if self.click:  # scale the mouseclick coordinates back to the original screen size
                    '''
                    Hier ist der Zustand des Spiels "nach Mausclick".
                    Das Mausclick wird hier nach der aktuelle Schirmgroesse skaliert.
                    '''
                    self.click = self.game_objekt.scale_click(self.click, self.game_objekt.screen_copy,
                                                              self.game_objekt.screen_via_display_set_mode)
                    x, y = self.click
                    self.game_objekt.check_num_buttons((x, y)) # pixel error might come from here?
                    x -= self.game_objekt.end_first_screen_part  # this offset is produced by the def of end_first_screen_part
                '''
                Das Mausclick wird hier zum Bearbeiten zum Game-Methode desk() geschickt und danach geloescht.
                '''
                self.game_objekt.desk(self.click)
                self.click = False
                # GEWINNVORAUSSETZUNG TESTEN
                if " ".join([word.name for word in self.game_objekt.guessed_code_words]) == self.game_objekt.woerter.code_satz:
                    self.won = True
                    self.wait = True


    def check_time_left(self, time_left=None):
        '''

        CHeckt, wie viele Zeit zum Spielen geblieben ist.
        Wenn keine, aendert den Spielzustand auf "verloren".
        '''
        if not time_left:
            time_left = self.game_objekt.time_left
        if time_left < 0:
            self.lost = True
            self.wait = True  # warten, bis der Spieler Space druckt

    def new_start(self): # Startet das ganze Spiel von neu, aber behaltet die Spielwoerter aus dem letzten
        '''
        Startet das Spiel erneut

        '''
        start_ticks = self.game_objekt.start_ticks # transfer the timer status  to the new game
        self.game_objekt = game.Game(self.input_codes, self.file_paths, self.binary_code, self.spielwoerter)
        self.game_objekt.start_ticks = start_ticks
        self.main_loop = False
        self.menu = True
        self.click = False
        self.binary_click = False
        self.wait = True
        print("new start")


    def move_things_left_and_right(self, ln, richtung): # stellt fest was die Links und Rechts Pfeilen machen
        '''
        Hier werden die Pfeile-Mausevents bearbeitet

        :param ln: die Laenge vom der Liste mit erratenen Code-Woerter (self.game_objekt.guessed_code_words)
        :param richtung: Die Pfeile-Richtung (links oder rechts)
        :return: None
        '''
        plusminus1 = 1 if richtung == K_RIGHT else -1 # diese Wert ist entweder 1 oder -1 abhängend davon, ob Links oder Rechts gedruckt wurde
        if self.game_objekt.word_to_move is not None: # checkt, ob der Spieler auf einem der Code_Wörter geklickt hat
            # wenn ja, checkt ob dieses Wort ausser die COde Wörter Liste verlassen würde, wenn es nach links oder rechts bewegt würde
            if self.game_objekt.word_to_move >= ln-1 and richtung == K_RIGHT:
                self.game_objekt.word_to_move = ln - 1
                insert_at = 0
            elif self.game_objekt.word_to_move <= 0 and richtung == K_LEFT:
                self.game_objekt.word_to_move = 0
                insert_at = ln-1
            else:
                insert_at = self.game_objekt.word_to_move + plusminus1
            popped = self.game_objekt.guessed_code_words.pop(self.game_objekt.word_to_move) # nimmt das geklickte Wort raus aus der Liste
            popped.color = self.game_objekt.orange
            try:
                self.game_objekt.guessed_code_words.insert(insert_at, popped) # fügt das geklickte Wort einen Platz nach links oder rechts
                self.game_objekt.word_to_move = insert_at
            except:
                print("out of bounds")
        else: # wenn es kein geklicktes Wort gibt, bewegt sich der Counter für Text-Fenster nach links oder nach rechts
            self.game_objekt.next_counter += plusminus1
            self.game_objekt.test_next_counter += plusminus1


