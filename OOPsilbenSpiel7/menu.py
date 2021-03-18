import pygame as pg

class Menu():
    def __init__(self, game_instance):
        self.info = game_instance
        #self.surface_cut = pg.Surface.subsurface(self.info.large_surface,pg.Rect(2000,0,3000,3000))
        self.offset = 0
        self.text_pos = (self.info.midtop[0], self.info.midtop[1] + self.offset + self.info.space)
        # keys
        self.move = "AWDS / LEFT RIGHT UP DOWN"
        self.verification_window = "V"
        self.verify_choice = "Y"
        self.workspace_window = "SPACE"
        self.cheating = "C"
        self.main_loop = "S"
        self.drop_objects = 0
        self.next, self.back = "LEFT", "RIGHT"
        self.accelerate,self.decelerate = "PLUS / 2", "MINUS / 1"
        self.instructions = "I"
        self.list_instructions = self.list_lists_instructions()

    def choose_language(self):
        blit_h1 = self.info.blit_clickable_words(f"Drücke D für Deutsch", self.info.zuff, (self.info.midtop[0],
                                                                                           self.info.midtop[1] + self.info.down * 2))
        #blit_h2 = self.info.blit_string_words(f"Press E for English (nicht fertig)",self.info.zuff,(self.info.midtop[0],
        #                    self.info.midtop[1]+ blit_h1))
        self.info.screen_transfer()

    def tutorial(self, next_counter, lang):
        self.info.screen_copy.fill(self.info.black)
        if next_counter > len(self.list_instructions[lang-1])-1:
            next_counter = 0
        elif next_counter < 0:
            next_counter = len(self.list_instructions[lang-1]) - 1
        blit_h = self.info.blit_clickable_words(self.list_instructions[lang - 1][next_counter], self.info.zuff, (self.info.midtop[0],
                                                                                                                 self.info.midtop[1] + self.info.down * 2), font=self.info.smaller_font)
        self.info.screen_transfer()
        return next_counter

    def overview(self): # all instructions in one window, then you can press a key to see the tutorial again
        pass

    def list_lists_instructions(self):
        dict = {}
        start = f"Willkommen zum Spielanleitung! Drücke {self.next} um fortzufahren oder {self.back} um zurückzugehen. Um die Anleitung zu SKIPPEN, drücke {self.main_loop}. "
        prerequisites = f"Wenn du das Spiel in einem Editor geöffnet hast, installiere Python v.3+, Pygame und wiktionary_de_parser. " \
                        f"Probiere die Verzeichnissnamen anzupassen, wenn sie als nicht gefundene bezeichnet werden. Drücke run in file main. "
        move = f"Um dich zu bewegen, nutze die {self.move} Tasten. Um schneller oder langsamer zu werden, nutze {self.accelerate} oder {self.decelerate}. " \
               " Warnung: Alles auf der Schirm wird seine Geschwindigkeit aendern. "
        goal = f"Dein Ziel ist, ein Code zu finden. Der Code sieht aus wie ein Satz. " \
                   f"Um den Satz zu bekommen, musst du die richtige Woerter in der richtigen Reihenfolge zusammensetzen. " \
               f"Die Woerter findest du, indem du Silben sammelst und sie ebenso zusammensetzest. Du kannst bis 12 Silben sammeln. " \
               f"Um sie zu entlasen, druecke {self.drop_objects}. "

        word_composing = f"Um deine gesammelte Silben zu sehen, druecke {self.workspace_window}. " \
                         f"Hier kannst du auf sie klicken, um aus denen ein Wort aufzubauen. Unter jedes Silbe wird Teil der Definition seines Wortes erscheinen. "
        code_word_composing = f"Wenn das Wort Teil des Code-Satzes ist, wird es statt eine Definition eine Instruktion haben. "
        word_guessing = f"Wenn ein Wort vollstaendig ist, aendert sich seine Farbe. Wenn Gold, ist es Teil des Code-Satzes. " \
                        f"Wenn Lila, ist es nicht. Alle erratene Woerter verschwinden aus dem Schirm. "
        verify_code = f"Um die erratene Woerter zu sehen, druecke {self.verification_window}. " \
                      f"Hier kannst du den Code-Satz aufbauen. Druecke auf dem Index vom Wort, das du umsetzen willst. " \
                      f"Dann druecke auf dem Index, an dem du es hinstellen willst. Druecke auf {self.back} und {self.next}, um die Instruktion zu sehen. "
        cheating = f"Druecke  {self.cheating}, um einen Hinweis zu bekommen. Dies kostet 5 Sekunden."
        game_window = f"Um das Spiel zu beenden, druecke auf X. Um die Schirmgroesse anzupassen, bewege die Schirmenden. " \
                      f"Um diese Anleitung nochmals zu sehen, druecke {self.instructions}. Druecke {self.main_loop} um zurueck zum Spiel zu gehen." \
                      f"Um fortzufahren, druecke jetzt {self.main_loop}. "

        list_de = [start, prerequisites, goal, move,word_composing,code_word_composing,word_guessing,verify_code,cheating, game_window]

        start = f"Welcome to the Game Tutorial! Press {self.next} to Continue or {self.back} to go Back. To skip the tutorial, press {self.main_loop}."
        prerequisites = f"If you have the game open in an editor, install Python v.3+, Pygame and the module wiktextract." \
                        f"Try to adjust the names of the directories if they are shown as not found. Run the program from file main."
        goal = f"The goal of this game is to assemble a secret code. The code is in the form of a sentence. " \
                   "To find the code, first collect objects. The objects that make up a word all have the same color." \
               "You need to collect them them in the right order to form a word. After you have all the code words, " \
               "put them in the right order to form the code sentence."
        move = f"To move, use the arrows or the ASWD keys. To change your speed, press {self.accelerate} or {self.decelerate}." \
               " Warning: this changes the speed of all objects."
        pick = f"Moving over an object picks it up. You can carry up to 12 objects at a time. You can release all the objects you carry " \
               f"by pressing {self.drop_objects}. To see and use your picked objects, press the {self.workspace_window} key to go to the workspace window. "
        word_composing = f"To compose a word in the workspace window, click on the objects. When you click on an object, " \
                  "part of the definition of its word will show up below it. If you click on the right objects in the right order, " \
                  "you will see the definition of a word start forming in the right order."
        code_word_composing = f"However, the secret code objects don't reveal parts of a word's definition when clicked. Instead, they reveal " \
                   "part of the instructions for the next stages of your adventure."
        word_guessing = f"If you compose a word, it will glow in a different color. Gold means that the word was part of the secret " \
                  "code sentence. Lila means that it was a decoy word. Every guessed word removes its objects from the playground " \
                  "and scores you points."
        verify_code = f"To see your guessed code words, press {self.verification_window} to go to the verification window. Here, you can put the code word_guessing in the " \
                      f"right order by clicking on a list of their numerical representations. Clicking on a word's index will select it; " \
                      f"clicking on another index will change its place to that index. Press the {self.back} and {self.next} arrows to see the " \
                      "part of the instructions each word carries."
        cheating = f"To cheat, press {self.cheating}. You will see the definition of a non-code word. If you have collected all non-code words, you will " \
                   "see the instruction bit for an index of the code sentence. Warning: cheating will cost you precious seconds."
        game_window = f"To exit the game, close the window using the X button. To resize the window, click on the edges and drag. " \
                      f"To see the instructions during the game, press {self.instructions}. Press {self.main_loop} to go back to the main game window at any point. " \
                      f"To start playing, press {self.main_loop} now."
        list_en = [start, prerequisites, goal, move,pick,word_composing,code_word_composing,word_guessing,verify_code,cheating, game_window]


        list_lists = [list_de,list_en]

        return list_lists




