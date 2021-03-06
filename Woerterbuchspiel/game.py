# -*- coding: utf-8 -*-
import random

import pygame as pg
import random
from pygame import *

from Woerterbuchspiel import globale_variablen, menu, silbe, spieler, woerter, word


class Game(globale_variablen.Settings):
    '''
    Diese Klasse ist eine Hilfklasse mit Methoden und Variablen
    fuer die Gameloop Klasse, wo das Spiel laeuft.
    Die Game Klasse vererbt die Settings Klasse, wo sich
    zusaetzliche allgemeine Werte und Funktionen befinden.
    '''
    def __init__(self, code_satz, file_paths, binary_code, dict):
        super().__init__()
        self.blink_counter = 0
        self.top = 0
        self.gw, self.nw = None, None
        self.h = 10 # (= die maximale Anzahl von Silben in einer der Spalten)
        self.change_color = True
        self.binary_code = binary_code
        self.code_satz = code_satz
        self.output_code = code_satz[0]
        self.next_counter = 0
        self.menu = menu.Menu(self)
        self.file_path = file_paths[0]
        self.syl_speed_change = 10
        self.initial_syl_speed_change = self.syl_speed_change
        # variables above may be needed to initialise other classes' instances
        self.spieler = spieler.Spieler(self)  # takes the game object as parameter
        self.empty_word_obj = word.Word("", "", [], 404, 404, self)
        self.woerter = woerter.Woerter(self, dict)
        self.words = self.woerter.words
        syls = self.woerter.silben + self.woerter.code_syls
        self.syls = random.sample(syls, len(syls))
        # self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.syl_pos_change = 0
        self.start_syls_cut_at = 0
        self.pos_list = self.get_pos_list()
        self.gold_syls, self.bad_syls = [], []
        self.columnWidth = self.screenw // 8
        self.end_first_screen_part = (self.columnWidth) * ((len(self.gold_syls) // self.h) + 1)
        self.start_third_screen_part = self.screenw - self.columnWidth * (len(self.bad_syls) // self.h + 1)
        self.end_header = self.down
        self.tript2 = self.screen_copy.subsurface(self.end_first_screen_part, self.end_header,
                                                  self.start_third_screen_part - self.end_first_screen_part, # times two?
                                                  self.screenh-self.end_header)
        self.header = self.screen_copy.subsurface(0, 0, self.screenw, self.end_header)
        self.tript1 = Surface((self.tript2.get_rect().w, self.tript2.get_rect().w),
                                          pg.SRCALPHA) # SRCALPHA initialises the surface to transparent
        self.tript1rect = Rect(0,0,self.end_first_screen_part,self.screenh)
        self.tript3 = Surface((self.tript2.get_rect().w, self.tript2.get_rect().w),
                                          pg.SRCALPHA)
        self.tript3rect = Rect(self.start_third_screen_part, 0, self.screenw-self.start_third_screen_part, self.screenh)
        self.screen_syls = self.get_screensyls()
        self.guessed_code_words = []
        self.buttons = []
        self.clicked_word_index = None
        self.step_fps = 1
        self.temp_update_code_defs = None
        self.text_snapshot_counter = 0
        self.attempted_word = self.empty_word_obj.make_blank_word()


    def desk(self, click):  # the click is adjusted for where it'd be on screen_copy
        '''
        Hier wird jedes Mausclick bearbeitet.
        Zudem wird der obene mittlere Teil des Schirms aktualisiert.

        :param click: Das Mausclick
        :return: None
        '''
        self.tript2.fill(self.dark)
        self.ziffern_und_code_woerter() # aktualisiert der obene mittlere Teil des Schirms (header)
        if click:
            x,y = click
            click_rect = Rect(x,y,1,1)
            all_syls = self.gold_syls + self.bad_syls
            collision = click_rect.collidelist(all_syls)
            if collision != -1:
                syl = all_syls[collision]
                if self.attempted_word.is_guessed:
                    self.attempted_word = self.empty_word_obj.make_blank_word()
                if syl.clicked_on:
                    syl.clicked_on = False
                    self.attempted_word.syls.remove(syl)
                else:
                    syl.clicked_on = True
                    self.attempted_word.syls.append(syl)
        if self.temp_update_code_defs or self.clicked_word_index:
            self.blit_code_text()
        else:
            self.check_word()
            self.blit_word(surface=self.tript2)

    def blit_word(self, surface=None):  # =None due to self.parameter not working (due to being out of the init?)
        '''
        Zeichnet die geclickten Silben in der Mitte des Schirms

        :param height_of_all: Das Ende des gezeichten Wortes (die Y-koordinate)
        :param surface: Der Schirm
        :return: None
        '''
        if self.attempted_word.is_guessed: farbe = (self.yellow, self.yellow)
        else: farbe = (self.lime, self.cyan)
        if not surface: surface = self.screen_copy
        word_img = self.default_font.render(self.attempted_word.name_from_syls, True, farbe[0])
        surface.blit(word_img, (surface.get_rect().center[0] - word_img.get_rect().w // 2, self.top))
        # (bug: when the middle screen is too small for an individual word, the word gets cut (using either of the blit functions)
        blit_h = self.blit_clickable_words(self.attempted_word.meaning, farbe[1], self.top + self.down,
                                           screen=surface,snapshots=True)  # starts one line below the blitted word per the function

    def check_word(self):
        '''
        Prueft, ob das aufgebaute Wort richtig ist.
        :return: None
        '''
        self.remove_word_from_lists_if_guessed(self.words)
        self.remove_word_from_lists_if_guessed(self.woerter.unguessed_code_words)

    def remove_guessed_word_syls_from_list(self, lst):
        for syl in self.attempted_word.syls:
            try:
                lst.remove(syl) # ValueError: list.remove(x): x not in list
            except: print("excepted ValueError: list.remove(x): x not in list")

    def remove_word_from_lists_if_guessed(self, lst):
        for word in lst:
            if word.tuples == self.attempted_word.tuples:
                self.attempted_word.is_guessed = True
                self.delete_word()
                lst.remove(word)
                if lst == self.woerter.unguessed_code_words:
                    self.guessed_code_words.append(word)
                    self.remove_guessed_word_syls_from_list(self.gold_syls)
                else:
                    self.remove_guessed_word_syls_from_list(self.bad_syls)

    def delete_word(self):  # same syl is actually different objects in different lists, why?
        '''
        Loescht ein erratenes Wort
        :return:
        '''
        self.sylscounter -= len(self.attempted_word.syls)
        for this in self.attempted_word.syls:
            if len(self.syls) < len(self.pos_list):
                replacement = silbe.Silbe("o", "word", ["bit"], 404, 404, self, self.dark)  # replace with simpler object?
                replacement.visible = False
                replacement.rect.w, replacement.rect.h = 1, 1
                index = self.syls.index(this)
                self.syls[index] = replacement
            else:
                self.syls.remove(this)
            self.spieler.my_silben.remove(this)

    def blit_code_text(self):
        guessed_code_words_definitions_ll = [bit for word in self.guessed_code_words[:] for bit in
                                             word.bits]
        guessed_code_words_definitions_l = [" ".join(lst) for lst in guessed_code_words_definitions_ll]
        guessed_code_words_definitions_str = " ".join(guessed_code_words_definitions_l)
        self.temp_update_code_defs = guessed_code_words_definitions_str
        blit_h = self.blit_clickable_words(guessed_code_words_definitions_str, self.yellow, self.top,
                                           screen=self.tript2,
                                           snapshots=True)  # starts one line below the blitted word per the function

    def blit_clickable_words(self, lst, color, height, afont=0, screen=None,
                             buttons=False, snapshots=False, start_end=None):
        '''
        Zeichnet eine String (z.Media. Anleitung-Saetze oder Wort-Definitionen) auf dem Schirm.
        Die gezeichneten Objekten (z.Media. Woerter) koennen auf Wunsch zum Button-Objekts werden,
        auf die man clicken kann. (die Button Klasse ist im file "word").

        :param lst: die String zum Zeichnen
        :param color: farbe
        :param height: bestimmt die Hoehe
        :param afont: der Font
        :param screen: der Schirm
        :param buttons: Buttons erzeugen oder nicht
        :param start_end: koordinaten, wo gezeichnet wird (bestimmt die Breite)
        :return: Das Ende des Gezeichnetes (Y-Koordinate)
        '''
        # variablen
        if not screen: screen = self.screen_copy
        copy_screen = screen.copy()
        if type(lst) == str: lst = lst.split(" ")
        if not afont: afont = self.smaller_font
        if start_end: start, end = start_end
        else: start, end = 0.25, 0.75
        # for loop
        last_line_down, snapshots_counter, list_snapshots_to_blit, list_buttons = self.loop_through_text_to_display(afont, color, copy_screen, end, height,
                                                                                                                    lst,height, screen, start)
        # blitting
        self.blit_text_snapshot(copy_screen, last_line_down, list_snapshots_to_blit, screen, snapshots,
                                snapshots_counter)
        # buttons
        if buttons: self.buttons = list_buttons
        # return lower end
        return last_line_down + self.font_spacing(afont)  # how far down the screen there is curently text

    def blit_text_snapshot(self, copy_screen, last_line_down, list_snapshots_to_blit, screen, snapshots,
                           snapshots_counter):
        if snapshots and snapshots_counter:
            snapshot_to_blit = self.divide_text_into_surfaces(list_snapshots_to_blit, copy_screen)
            self.blit_snapshots_arrows(snapshot_to_blit, last_line_down)
        else:
            snapshot_to_blit = copy_screen.copy()
        screen.blit(snapshot_to_blit, (0, 0))

    def blit_snapshots_arrows(self,screen,last_line_down):
        y = 0.1* (self.screenh - self.end_header)
        x = 0.1*self.tript2.get_rect().right

        draw.polygon(screen,self.orange,((9*x,6*y),(9.5*x,5.5*y),(10*x,6*y)))
        draw.polygon(screen, self.orange, ((9 * x, 6.5 * y), (9.5 * x, 7 * y), (10 * x, 6.5 * y)))



    def loop_through_text_to_display(self, afont, color, copy_screen, end, last_line_down,
                                     lst, height, screen, start):
        x,y,w,h = copy_screen.get_rect()
        spacing = self.font_spacing(afont)
        last_word_right = start * w
        snapshots_counter = 0
        list_snapshots_to_blit = {}
        buttons = []
        color_copy = color
        for i in range(len(lst)):
            aword = lst[i]
            if not aword: continue
            if type(aword) is word.Word:
                if aword.color: color = aword.color
                aword = aword.name
            elif aword.isupper() or aword[0].isdigit():
                color = self.lime
            word_img = afont.render(f'{aword} ', True, color)
            word_rect = word_img.get_rect()
            color = color_copy
            if last_word_right + word_rect.w >= end * w:
                if last_line_down < h - spacing * 3:  # twice the highest spacing?
                    last_word_right = start * w
                    last_line_down += spacing
                else:
                    copy_screen = screen.copy()
                    last_line_down = height
                    last_word_right = start * w
                    snapshots_counter += 1
            word_rect.x, word_rect.y = last_word_right, last_line_down
            buttons.append(word.Button(aword, word_img, word_rect, i))
            copy_screen.blit(word_img, word_rect)
            last_word_right = last_word_right + word_rect.w  # + afont.render(" ",True,self.white).get_rect().w
            if aword[-1] in ".!?:":  # mache eine neue Zeile nach diesen SYmbolen
                last_word_right = start * w
                last_line_down += spacing * 1.5
            list_snapshots_to_blit[snapshots_counter] = copy_screen.copy()
        return last_line_down, snapshots_counter, list_snapshots_to_blit, buttons

    def divide_text_into_surfaces(self, list_snapshots_to_blit, screen):
        if len(list_snapshots_to_blit) == 0:
            return screen.copy()
        if self.text_snapshot_counter < 0:  # temp? counter adjusts the text window counter without changing it, so that it doesnt keep resetting to the first or last window when it's outside the bounds
            self.text_snapshot_counter = len(list_snapshots_to_blit) - 1
        elif self.text_snapshot_counter > len(list_snapshots_to_blit) - 1:
            self.text_snapshot_counter = 0
        return list_snapshots_to_blit[self.text_snapshot_counter]

    def blink(self, num_steps, syl, new_color, start_color=None):
        '''
        Bringt ein Silbe-Objekt zum Blinken (d.h. seine Farbe auf der Startfarbe
        langsam nach der Zielfarbe aendern).
        Gesehen hier: https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        :param num_steps: die Spielmomente (FPS), die es dauern soll, bis die Zielfarbe erreicht wird
        :param syl: die Silbe
        :param new_color: die Zielfarbe
        :param start_color: die Startfarbe
        :return: die aktuelle Farbe der Silbe (meist zwischen der Startfarbe und der Zielfarbe)
        '''
        if not start_color:
            start_color = syl.rgb
        list_ints = [
            int(orig_rgb_digit + (new_rgb_digit - orig_rgb_digit) * self.step_fps / num_steps) for
            orig_rgb_digit, new_rgb_digit in list(zip(start_color, new_color))]  # see stackoverflow link on fading
        try:
            list_ints[0], list_ints[1], list_ints[2] in range(0, 255)
        except:
            print("excepted rgb for", syl.name, ":", list_ints[0], list_ints[1], list_ints[2])
        if self.change_color:  # step fps changes in the direction towards the new color
            if self.step_fps < num_steps:  # self fps hasn't reached the new color yet
                self.step_fps += 1
            else:  # the change is complete, but the bool shouldn't be flipped until a second has passed
                if not self.blink_counter:  # blink counter starts counting for a second
                    self.blink_counter = 1
                elif self.blink_counter >= self.fps // 2:  # blink counter has finished counting for a time unit
                    self.change_color = False
        else:
            if self.step_fps > 0:  # step fps is changing in the direction of the original color
                self.step_fps -= 1
            elif self.step_fps == 0:
                if not self.blink_counter:  # blink counter starts counting for a second
                    self.blink_counter = 1
                elif self.blink_counter >= self.fps // 2:  # blink counter has finished counting for a time unit
                    self.change_color = True
                    self.blink_counter = None  # reset blink counter to None so it can start counting again at the right time
        return (list_ints[0], list_ints[1], list_ints[2])

    def get_pos_list(self):
        '''
        Erzeugt die Startpositionen der sich bewegenden Silbe-Objekte
        :return: die Startpositionen
        '''
        poslist = []
        space = self.screenh // self.h
        pos = self.screenh
        while pos >= 0 - self.syl_pos_change:
            poslist.append(pos)
            pos -= space
        return poslist

    def get_screensyls(self):
        '''
        Bereitet Silbe-Objekte, die auf dem Schirm im Bewegung gezeichnet werden.
        Sie sind so ausgewaehlt, dass wenn die untersten-gezeichnete den Schirm verlaesst,
        wird sie aus der Liste ausgeschlossen und eine neue am Anfang hinzugefuegt.
        :return: Silben fuer den sich bewegenden Loop
        '''
        syls = self.syls[self.start_syls_cut_at:] + self.syls[:self.start_syls_cut_at]
        # syls = [syl for syl in syls if syl.visible] #why does this make the loop jerk backwards?
        to_return = syls[:len(self.pos_list)]
        for syl in to_return:
            if syl.visible:
                too_left = syl.rect.x < self.end_first_screen_part
                too_right = syl.rect.x > self.start_third_screen_part - syl.rect.w
                if too_left:
                    while syl.rect.x < self.end_first_screen_part:
                        syl.rect.x += self.screenw // self.columnWidth
                elif too_right:
                    while syl.rect.x > self.start_third_screen_part - syl.rect.w:
                        syl.rect.x -= self.screenw // self.columnWidth
                if syl.rect.x < self.end_first_screen_part or syl.rect.x > self.start_third_screen_part - syl.rect.w:
                    self.end_first_screen_part = self.start_third_screen_part - syl.rect.w  # trigger new game?
        return to_return  # (now syls should always be bigger than this cut)

    def blit_loop(self):
        '''
        Zeichnet den ganzen sich bewegenden Loop
        :return:
        '''
        #self.screen_copy.fill(self.white)
        self.screen_copy.blit(self.hintergrund, (0, 0))
        self.screen_copy.blit(self.tript1,self.tript1rect)
        self.screen_copy.blit(self.tript3, self.tript3rect)
        self.blit_loop_middle()
        self.blit_loop_left()
        self.blit_loop_right()
        self.adjust_loop_window()
        self.screen_copy.blit(self.spieler.image, self.spieler.rect)
        self.resize_and_display_screen()

    def blit_loop_middle(self):
        '''
        Zeichnet der mittlere Teil des Loops
        :return: None
        '''
        # variablen
        self.screen_syls = self.get_screensyls()
        # for loop
        for i in range(len(self.pos_list)):
            if self.screen_syls:
                syl = self.screen_syls.pop(0)
                circle_width = 2
                if syl.visible:
                    if syl.tuple in [s.tuple for s in self.woerter.code_syls]:
                        syl.rgb = self.blink(self.fps * 2, syl,
                                             self.yellow)  # das erste Argument ist die Dauer des Blinkens
                        syl.image = self.default_font.render(syl.name, True, tuple(syl.rgb))
                        circle_width = int(
                            2 + (self.step_fps // self.fps * 2) * 2)  # width goes up and down with the color changes
                    self.screen_copy.blit(syl.image, (syl.rect.x, self.pos_list[i] + self.syl_pos_change))
                    try:
                        draw.circle(self.screen_copy, syl.rgb, syl.rect.center, syl.rect.w, width=circle_width)
                    except: pass
                elif syl.picked:  # picked ist eine zahl zwischen 0 und self.fps
                    try: # had error "Nonetype object has no center" when the direction was upwards
                        draw.circle(self.screen_copy, syl.rgb, syl.new_spot_rect.center, syl.rect.w // 2, width=syl.picked)
                        draw.circle(self.screen_copy, syl.rgb, syl.ghost_rect.center, syl.rect.w, width=syl.picked)
                    except: pass
                    # TODO 'NoneType' bug: object has no attribute 'center' sometime after loop direction reversal
                    syl.picked = syl.picked - 4 if syl.picked > 0 else 0
                syl.rect.y = self.pos_list[
                                 i] + self.syl_pos_change  # syl moves to the current ratio of start_pos/movement_window
                syl.rect_in_circle.center = syl.rect.center
                syl.rect_copy = syl.rect.copy()  # why does this leave rect in place

    def blit_loop_right(self):
        '''
        Zeichnet der rechte Teil des Loops
        :return:
        '''
        lil = self.bad_syls[:]
        lila_tuples = [syl.tuple for syl in lil]
        non_code_tuples = [word.tuples for word in self.words]

        # Die lambda funktion berechnet die X koordinate der silben. Sie nimmt ein parameter namens "rowIndex" (in der definition von blit_trypt() )
        self.blit_loop_one_side(True, lil, self.nw, lambda columnIndex: self.screenw - self.columnWidth - columnIndex * self.columnWidth, lila_tuples, non_code_tuples)

    def blit_loop_left(self):
        '''
        Zeichnet der linke Teil des Loops
        :return: None
        '''
        gold = self.gold_syls[:]
        gold_tuples = [syl.tuple for syl in gold]
        code_tuples = [w.tuples for w in self.woerter.unguessed_code_words]

        self.blit_loop_one_side(False, gold, self.gw, lambda columnIndex: columnIndex * self.columnWidth, gold_tuples, code_tuples)

    def blit_loop_one_side(self, list_ist_lila, lst_syls, blinking_word, x_position, syl_tuples, words_tuples):
        '''
        Zeichnet der linke oder der Rechte Teil des Loops (je nachdem,
        ob der Argument "list_ist_lila" True oder Falsch ist)
        :param list_ist_lila: bestimmt, welcher Teil des Schirms gezeichnet wird
        :param lst_syls: die Silbe-Objekte zum zeichnen
        :param blinking_word: die blinkenden Silben
        :param x_position: der Index der Reihe, wo eine Silbe gezeichnet wird
        :param syl_tuples: die Tuple-eigenschaften von den Silbe-Objekten
        :param words_tuples: die Tuple-eigenschaften von allen Silbe-Objekten, die ein Wort aufbauen
        :return: None
        '''
        if (not blinking_word) or blinking_word[
            0] not in syl_tuples:  # falls zumindest eine tuple vom blinking word gelöscht wurde
            # Diese if Klause versucht, nur eine Silbe pro Sektor zum blinken zu bringen. Jedoch blinken im Moment mehrere...
            blinking_word = self.find_complete_syls(syl_tuples, words_tuples)
            if list_ist_lila:
                self.nw = blinking_word  # self.nw ist die gespeicherte blinkende Silbe auf dem rechten Sektor
            else:
                self.gw = blinking_word  # self.gw ist die gespeicherte blinkende Silbe auf dem linken Sektor
        len_lst_syls = len(lst_syls)
        # go through each of h elements because in each column we have h elements
        # calculate the column index by syl_index_at_intersection_of_row_and_column//h -> 0,1,2,3
        for row_index in range(0, self.h):
            for column_index in range(0, len_lst_syls):
                syl = Game.get_syl(column_index,row_index,lst_syls, self.h)
                if syl is None:
                    break
                syl.rect.x = x_position(column_index)
                if blinking_word and syl.tuple in blinking_word:
                    syl.rgb = self.blink(self.fps * 2, syl, self.red, start_color=self.cyan)
                    syl.image = self.default_font.render(syl.name, True, tuple(syl.rgb))
                syl.rect.y = self.top + row_index * ((self.screenh - self.top) // self.h)
                self.screen_copy.blit(syl.image, syl.rect)

    def adjust_loop_window(self):  # Verwaltet den laufenden Loop aus runterfallenden Silben
        '''
        Aendert die Variable, die der Anfang der Liste aus laufenden Silben bestimmt (self.start_syls_cut_at)
        und die der Abstand zwischen einer Startposition und die aktuelle Position der Silben bestimmt (self.syl_pos_change)
        :return: None
        '''
        self.syl_pos_change += self.syl_speed_change  #
        if self.syl_pos_change >= self.screenh // self.h:  # wenn
            self.syl_pos_change = 0
            self.start_syls_cut_at += 1
            if self.start_syls_cut_at > len(self.syls) - 1:  # "==" doesn't work after words get deleted
                self.start_syls_cut_at = 0
        elif self.syl_pos_change <= - self.screenh // self.h:
            self.syl_pos_change = 0
            self.start_syls_cut_at -= 1
            if self.start_syls_cut_at < 1:  # "==" doesn't work after words get deleted
                self.start_syls_cut_at = len(self.syls) - 1

    def find_complete_syls(self, syl_tuples,
                           words_tuples):  # Findet ein kompletes Code-Wort in den gesammelten Code-Silben
        '''
        Checkt, ob aus gen vom Spieler gesammelten Silben ein (oder mehrere) ganze Woerter aufgebaut
        werden koennen. Wenn ja, nimmt die Silben aus dem ersten solchen Wort.
        :param syl_tuples: die Tuple-eigenschaften von den Silbe-Objekten
        (Sie sind ein Weg, das Objekt zu identifizieren)
        :param words_tuples: die Tuple-eigenschaften von allen Silbe-Objekten, die ein Wort aufbauen
        :return:
        '''
        random.shuffle(words_tuples)  # sodass die reihenfolge der blinkenden gesammelten code woerter zufaellig ist
        try:
            nxt = next(iter([set for set in words_tuples if
                             [t for t in set if t in syl_tuples] == [t for t in set]]))  # ergibt eine Liste aus Tuples
            return nxt
        except:
            return None

    @classmethod
    def get_syl(cls, column_index, row_index, lst_syls, n_elements_in_column):
        '''
        Findet die Silbe in einer Liste mit bestimmten Reihe- und Spalte-Indexen
        '''
        len_lst_syls = len(lst_syls)
        syl_index_at_intersection_of_row_and_column = column_index * n_elements_in_column + row_index
        if syl_index_at_intersection_of_row_and_column >= len_lst_syls:
            return None
        syl = lst_syls[syl_index_at_intersection_of_row_and_column]
        return syl

    def game_over(self, text, surface=None):
        '''
        Zeichnet ein Zeichen, dass das Spiel beendet hat
        :param text: das Zeichen
        :param surface: der Schirm
        :return: None
        '''
        rect = Rect(0.33 * self.screenw, 0.33 * self.screenh, 0.66 * self.screenw, 0.33 * self.screenh)
        rect.center = self.screen_rect.center
        offset = 0.03 * self.screenh
        border_rect = Rect(rect.x - offset, rect.y - offset, rect.w + offset * 2, rect.h + offset * 2) # wrong dimensions?
        draw.rect(self.screen_copy, self.navy, border_rect)
        surface = self.screen_copy.subsurface(rect)
        surface.fill(self.gray)
        self.blit_clickable_words(text, self.white, self.down, screen=surface)

    def ziffern_und_code_woerter(self): # TODO combine the definitions underneath after clicking in the header
        '''
        Erzeugt der Header (obene Teil des Schirms) mit dem vom letzten Spiel uebernommene Code
        und das neue Code aus gesammelten Code-Woerter
        :return: None
        '''
        # if the header changes size, the subsurface may end up larger than the surface unless the function is called in the while loop
        # WOERTERBUCH MIT CODE WOERTER UND ZIFFERN ERSTELLEN
        self.screen_copy.fill(self.black, Rect(0, 0, self.screenw, self.end_header))
        digits_line = self.font_spacing(self.bigger_font)
        neu_list = [" NEU >>> "]
        rendered_alt = self.bigger_font.render(" ALT >>>> ", True, self.cyan)
        self.screen_copy.blit(rendered_alt, (0, digits_line))
        digit_identation = rendered_alt.get_rect().w

        for i in range(len(self.woerter.all_code_words)):  # füllt den Woerterbuch auf
            code_number_at_this_index = list(self.binary_code)[i]
            temporary_code_number = 0 if code_number_at_this_index == '1' else 1
            if i < len(self.guessed_code_words):  # diese Klause umfasst die code-woerter die moeglicherweise erraten wurden
                dieses_code_wort = self.guessed_code_words[i]
                neu_list.append(dieses_code_wort)
                space_nach_ziffer = self.bigger_font.render(f'{dieses_code_wort.name} ', True, self.dark).get_rect().w
                if dieses_code_wort == self.woerter.all_code_words[i]:
                    temporary_code_number = code_number_at_this_index
            else:
                ziffer = f'{i + 1}'
                space_nach_ziffer = self.bigger_font.render(ziffer, True, self.dark).get_rect().w

            self.screen_copy.blit(self.bigger_font.render(f'{temporary_code_number}', True, self.cyan),
                                  (digit_identation, digits_line))
            digit_identation += space_nach_ziffer

        self.end_header = self.blit_clickable_words(
            [a for a in neu_list], self.yellow, digits_line*2, buttons = True, start_end=(0, 100), afont=self.bigger_font)


    def check_num_buttons(self,
                          click):  # the buttons were made using coordinates starting from 0,0 in the screen given to blit_words()
        '''
        Prueft, ob auf einem Button-Objekt geclickt wurde. Wenn ja, speichert der Index von diesem Objekt
        in der Variabel "self.clicked_word_index"
        :param click: das Mausclick
        :return: None
        '''

        if self.buttons:  # self.buttons only refers to the guessed code words on trypt2
            for each in self.guessed_code_words: each.color = None
            click_rect = Rect(click[0], click[1], 1, 1)
            index = click_rect.collidelist([a.rect for a in self.buttons])
            # das "-1" kompensiert dafür, dass der erste object im self.buttons ("NEU>>>") nicht berücksichtigt wird
            if index != -1 and index != 0: # "-1" bedeutet keine Kollision und "0" bedeutet das nicht zu berücksichtigen element "NEU>>>"
                self.clicked_word_index = index - 1 # index wird in guessed_code_words benutzt, wo "NEU>>>" nicht existiert
                self.guessed_code_words[self.clicked_word_index].color = self.red
            elif self.clicked_word_index:
                self.clicked_word_index = None
                self.temp_update_code_defs = None


    def localised_instructions(self):
        '''
        Zeichnet Anleitungen fuer die verschiedenen Bereichen des Spiels jeweils in dem richtigen Bereich
        :return: None
        '''

        text_header = "Die Code-Wörter werden unter den Ziffern erscheinen, nachdem du sie aufbaust. " \
                      "Klicke auf ein Wort und bewege es mit den Pfeiltasten, um die Reihenfolge zu ändern. "
        text_left = "Hier erscheinen die gesammelten Code-Silben. " \
                    "Aus denen besteht den Code-Satz, den du brauchst. " \
                    "Du musst aus den Code-Silben die Code-Wörter aufbauen. "
        text_right = "Hier erscheinen die Silben, die du vermeiden solltest. " \
                     "Mache Wörter aus ihnen, um sie zu entfernen. "
        text_middle = "Bewege dich mit den Pfeiltasten. " \
                      "Nutze w und s für die Geschwindigkeit. " \
                      "Sammele Code-Silben. Sie blinken in gelb. " \
                      "Vermeide die anderen Silben, um nicht zu verlieren. " \
                      "KLICKE auf die gesammelten Silben, um ein Wort aufzubauen. " \
                      "Du kannst auf sie klicken, nachdem du mit der LEERTASTE den Action-Modus verlässt. " \
                      "Wenn du fertig bist, gehe zurück in den Action-Modus mit der Leertaste. " \
                      "Wenn du blinkende Silben siehst, ist dies ein Hinweis. " \
                      "Sie sind Teil von demselben Wort. " \
                      "Nachdem unter den Ziffern deine Code-Wörter erscheinen, kannst du auf sie klicken und bewegen. " \
                      "Wenn du das tust, siehst du in der Mitte einen ungeordneten Text. " \
                      "Wenn du den Codesatz in die richtige Reihenfolge bringst, wird auch der Codetext in der richtigen Reihenfolge."


        text_and_locations = {
            text_header: self.header,
            text_left: self.screen_copy.subsurface(0,self.end_header,self.end_first_screen_part,self.screenh-self.end_header),
            text_right: self.screen_copy.subsurface(self.start_third_screen_part,self.end_header,
                                                    self.screenw-self.start_third_screen_part,self.screenh-self.end_header),
            text_middle: self.tript2
        }
        text_and_colors = {text_header:self.black,text_left:self.navy,text_middle:self.dark,text_right:self.navy}
        for key in text_and_locations.keys():
            text_and_locations[key].fill(text_and_colors[key])
            self.blit_clickable_words(key,self.white,0.3*self.down,screen=text_and_locations[key],
                                      start_end=(0.1,0.9),snapshots=True)
