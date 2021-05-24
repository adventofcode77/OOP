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
        self.radiuses = []
        self.blink_counter = 0
        self.top = 0
        self.gw, self.nw = None, None
        self.h = 10 # (= die maximale Anzahl von Silben in einer der Spalten)
        self.change_color = True
        self.binary_code = binary_code
        self.code_satz = code_satz
        self.output_code = code_satz[0]
        self.next_counter = 0
        self.test_next_counter = 0
        self.menu = menu.Menu(self)
        self.file_path = file_paths[0]
        self.syl_speed_change = 10
        self.initial_syl_speed_change = self.syl_speed_change
        # variables above may be needed to initialise other classes' instances
        self.spieler = spieler.Spieler(self)  # takes the game object as parameter
        self.spielwoerter = dict
        self.woerter = woerter.Woerter(self)
        self.words = self.woerter.words
        syls = self.woerter.silben + self.woerter.code_syls
        self.syls = random.sample(syls, len(syls))
        self.silben_copy, self.code_silben_copy, self.syls_copy = self.woerter.silben[:], self.woerter.code_syls[
                                                                                          :], self.syls[:]
        # self.syls = silbe.Silbe.silbe_all_syls # why does this cause errors compared to self.bank.silben?
        self.sylscounter = len(self.syls)
        self.syl_pos_change = 0
        self.deleted_word_bool = False
        self.deleted_code_word_bool = False
        self.deletedlist = []
        self.deleted_word = ""
        self.start_syls_cut_at = 0
        self.pos_list = self.get_pos_list()
        self.gold_syls, self.lila_syls = [], []
        self.columnWidth = self.screenw // 8
        self.end_first_screen_part = (self.columnWidth) * ((len(self.gold_syls) // self.h) + 1)
        self.start_third_screen_part = self.screenw - self.columnWidth * (len(self.lila_syls) // self.h + 1)
        self.tript2 = self.screen_copy.subsurface(self.end_first_screen_part, 0,
                                                  self.start_third_screen_part - self.end_first_screen_part, # times two?
                                                  self.screenh)
        self.end_header = self.down
        self.header = self.screen_copy.subsurface(0, 0, self.screenw, self.end_header)
        self.screen_syls = self.get_screensyls()
        self.guessed_code_words = []
        self.buttons = []
        self.word_to_move = None
        self.step_fps = 1
        self.temp_update_code_defs = None
        self.text_snapshot_counter = 0


    def desk(self, click):  # the click is adjusted for where it'd be on screen_copy
        '''
        Hier wird jedes Mausclick bearbeitet.
        Zudem wird der obene mittlere Teil des Schirms aktualisiert.

        :param click: Das Mausclick
        :return: None
        '''
        self.tript2.fill(self.dark)
        self.ziffern_und_code_woerter() # aktualisiert der obene mittlere Teil des Schirms (header)
        # if self.temp:
        #     print("in game temp")
        #     temper = self.temp
        #     tempest = Rect(self.end_header,self.end_first_screen_part,self.screenh-self.end_header,self.start_third_screen_part-self.end_first_screen_part)
        #     self.screen_copy.fill(self.black,tempest)
        #     self.blit_clickable_words(temper,self.yellow,self.screen_rect.center,screen=self.tript2)
        if click:
            x, y = click
            for syl in self.gold_syls + self.lila_syls:
                if syl.rect.collidepoint(x, y):
                    if syl.clicked_on:
                        syl.clicked_on = False
                        index = self.spieler.appendlist.index(syl)
                        del self.spieler.appendlist[index]
                    else:
                        syl.clicked_on = True
                        self.draw_word(height_of_all=self.top, syl=syl, screen=self.tript2)
        self.draw_word(height_of_all=self.top, screen=self.tript2)

    def draw_word(self, height_of_all=None, syl=None, screen=None):
        '''
        Zeichnet die geclickten Silben in der Mitte des Schirms

        :param height_of_all: Das Ende des gezeichten Wortes (die Y-koordinate)
        :param syl: Ein SIlbe-Objekt
        :param screen: Der Schirm
        :return: None
        '''
        # TODO make object word_on_screen and keep the variables that define its state inside of it
        if not height_of_all:
            height_of_all = self.down
        if syl:
            self.spieler.appendlist.append(syl)
            if self.deleted_word_bool or self.deleted_code_word_bool:
                self.deleted_word_bool = False
                self.deleted_code_word_bool = False
                self.deletedlist = []
                self.deleted_word = ""
            self.check_word()
        if not screen:
            screen = self.screen_copy
        self.blit_word(height_of_all, surface=screen)

    def make_def_list(self):
        '''
        Erzeugt eine Liste mit Teilen von der Definition des Wortes
        :return: diese Liste
        '''
        if self.deleted_word_bool or self.deleted_code_word_bool:
            bitlists = [word for a in self.deletedlist[:] for word in a.bit]
        else:
            bitlists = [word for a in self.spieler.appendlist[:] for word in a.bit]
        return bitlists

    def blit_word(self, height_of_all=0,
                  surface=None):  # =None due to self.parameter not working (due to being out of the init?)
        '''
        Zeichnet die geclickten Silben (als Teil der draw_word() Methode)

        :param height_of_all: Das Ende des gezeichten Wortes (die Y-koordinate)
        :param surface: Der Schirm
        :return: None
        '''
        if self.deleted_word_bool or self.deleted_code_word_bool:
            farbe = (self.yellow, self.yellow)
            word_string = self.deleted_word
        else:
            farbe = (self.lime, self.cyan)
            word_string = "".join([a.name for a in self.spieler.appendlist])
        if not surface:
            surface = self.screen_copy
        word_img = self.default_font.render(word_string, True, farbe[0])
        if self.temp_update_code_defs or self.word_to_move:

            guessed_code_words_definitions_ll = [bit for word in self.guessed_code_words[:] for bit in
                                                 word.bits]
            guessed_code_words_definitions_l = [" ".join(lst) for lst in guessed_code_words_definitions_ll]
            guessed_code_words_definitions_str = " ".join(guessed_code_words_definitions_l)
            self.temp_update_code_defs = guessed_code_words_definitions_str
            temper = self.temp_update_code_defs
            blit_h = self.blit_clickable_words(temper, farbe[1], (
                self.screen_copy.get_rect().center[0], self.end_header+0.5*self.down),
                                               screen=surface,snapshots=True)  # starts one line below the blitted word per the function
        else:
            surface.blit(word_img, (
                surface.get_rect().center[0] - word_img.get_rect().w // 2, height_of_all + self.down))
            height_of_all += self.down * 2
            blit_h = self.blit_clickable_words(self.make_def_list(), farbe[1], (
                self.screen_copy.get_rect().center[0], max(self.screen_copy.get_rect().center[1], height_of_all)),
                                               screen=surface)  # starts one line below the blitted word per the function

    def blit_clickable_words(self, lst, color, midtop, afont=0, screen=None,
                             no_buttons=True, snapshots=False,start_end=None):
        '''
        Zeichnet eine String (z.Media. Anleitung-Saetze oder Wort-Definitionen) auf dem Schirm.
        Die gezeichneten Objekten (z.Media. Woerter) koennen auf Wunsch zum Button-Objekts werden,
        auf die man clicken kann. (die Button Klasse ist im file "word").

        :param lst: die String zum Zeichnen
        :param color: farbe
        :param midtop: koordinaten, wo gezeichnet wird (bestimmt die Hoehe)
        :param afont: der Font
        :param screen: der Schirm
        :param no_buttons: Buttons erzeugen oder nicht
        :param start_end: koordinaten, wo gezeichnet wird (bestimmt die Breite)
        :return: Das Ende des Gezeichnetes (Y-Koordinate)
        '''
        # variablen
        if not screen: screen = self.screen_copy
        copy_screen = screen.copy()
        copy_screen_rect = copy_screen.get_rect()
        if no_buttons: copy_buttons = self.buttons[:]
        self.buttons = []
        if type(lst) == str: lst = lst.split(" ")
        color_copy = color
        if not afont: afont = self.smaller_font
        spacing = self.font_spacing(afont)
        last_line_down = midtop[1]
        if start_end: start, end = start_end
        else: start, end = 0.25, 0.75
        last_word_right = start * copy_screen_rect.w
        # for loop
        last_line_down, snapshots_counter, list_snapshots_to_blit = self.loop_through_text_to_display(afont, color, color_copy, copy_screen,
                                                                           copy_screen_rect, end, last_line_down,
                                                                           last_word_right, lst,
                                                                           midtop, screen, spacing, start)
        # snapshots
        if snapshots and snapshots_counter:
            snapshot_to_blit = self.divide_text_into_surfaces(list_snapshots_to_blit, copy_screen)
            self.blit_snapshots_arrows(snapshot_to_blit,last_line_down)
        else:
            snapshot_to_blit = copy_screen.copy()
        screen.blit(snapshot_to_blit, (0, 0))
        # buttons
        if no_buttons:
            self.buttons = copy_buttons
        return last_line_down + self.font_spacing(afont)  # how far down the screen there is curently text

    def blit_snapshots_arrows(self,screen,last_line_down):
        y = 0.1* (self.screenh - self.end_header)
        x = 0.1*self.tript2.get_rect().right

        draw.polygon(screen,self.orange,((8*x,6*y),(8.5*x,5.5*y),(9*x,6*y)))
        draw.polygon(screen, self.orange, ((8 * x, 6.5 * y), (8.5 * x, 7 * y), (9 * x, 6.5 * y)))



    def loop_through_text_to_display(self, afont, color, color_copy, copy_screen, copy_screen_rect, end, last_line_down,
                                     last_word_right, lst, midtop, screen, spacing, start):
        snapshots_counter = 0
        list_snapshots_to_blit = {}
        for i in range(len(lst)):
            aword = lst[i]
            if not aword: continue
            if type(aword) is word.Word:
                if aword.color:
                    color, aword = aword.color, aword.name
                    print("blitclick", color, aword)
            elif aword.isupper() or aword[0].isdigit():
                color = self.lime
            word_img = afont.render(f'{aword} ', True, color)
            word_rect = word_img.get_rect()
            color = color_copy
            if last_word_right + word_rect.w >= end * copy_screen_rect.w:
                if last_line_down < copy_screen_rect.h - spacing * 3:  # twice the highest spacing?
                    last_word_right = start * copy_screen_rect.w
                    last_line_down += spacing
                else:
                    copy_screen = screen.copy()
                    last_line_down = midtop[1]
                    last_word_right = start * copy_screen_rect.w
                    snapshots_counter += 1
            word_rect.x, word_rect.y = last_word_right, last_line_down
            self.buttons.append(word.Button(aword, word_img, word_rect, i))
            copy_screen.blit(word_img, word_rect)
            last_word_right = last_word_right + word_rect.w  # + afont.render(" ",True,self.white).get_rect().w
            if aword[-1] in ".!?:":  # mache eine neue Zeile nach diesen SYmbolen
                last_word_right = start * copy_screen_rect.w
                last_line_down += spacing * 1.5
            list_snapshots_to_blit[snapshots_counter] = copy_screen.copy()
        return last_line_down, snapshots_counter, list_snapshots_to_blit

    def divide_text_into_surfaces(self, list_snapshots_to_blit, screen):
        if len(list_snapshots_to_blit) == 0:
            return screen.copy()
        if self.text_snapshot_counter < 0:  # temp? counter adjusts the text window counter without changing it, so that it doesnt keep resetting to the first or last window when it's outside the bounds
            self.text_snapshot_counter = len(list_snapshots_to_blit) - 1
        elif self.text_snapshot_counter > len(list_snapshots_to_blit) - 1:
            self.text_snapshot_counter = 0
        return list_snapshots_to_blit[self.text_snapshot_counter]


    def check_word(self):
        '''
        Prueft, ob das aufgebaute Wort richtig ist.
        :return: None
        '''
        temp_bool = True
        appendlisttuples = [a.tuple for a in self.spieler.appendlist]
        for word in self.words:  # check for the word in non-code words
            wordtuples = [a.tuple for a in word.syls]  # 1 comparison with wordtuples for each word in words
            if appendlisttuples == wordtuples:
                self.deleted_word = word.name
                self.delete_word()
                self.words.remove(word)  # words is used only for cheating
                self.deleted_word_bool = True
                temp_bool = False
        if temp_bool:
            for word in self.woerter.code_words:  # check in code words
                wordtuples = [a.tuple for a in word.syls]
                if appendlisttuples == wordtuples:
                    self.deleted_word = word.name
                    self.delete_word()
                    self.woerter.code_words.remove(word)
                    self.guessed_code_words.append(word)
                    self.deleted_code_word_bool = True

    def delete_word(self):  # same syl is actually different objects in different lists, why?
        '''
        Loescht ein erratenes Wort
        :return:
        '''
        for this in self.spieler.appendlist:
            for syl in self.syls:
                if this.tuple == syl.tuple:
                    index = self.syls.index(syl)
                    if len(self.syls) < len(self.pos_list):
                        replacement = silbe.Silbe("o", "word", ["bit"], 404, 404, self,
                                                  (0, 0, 0))  # replace with simpler object?
                        replacement.visible = False
                        replacement.rect.x, replacement.rect.y = 1, 1
                        self.syls[index] = replacement
                    else:
                        self.syls.remove(syl)
                    self.sylscounter -= 1
            for syl in self.spieler.my_silben:
                if this.tuple == syl.tuple:
                    self.spieler.my_silben.remove(syl)
            for syl in self.gold_syls:
                if this.tuple == syl.tuple:
                    self.gold_syls.remove(syl)
            for syl in self.lila_syls:
                if this.tuple == syl.tuple:
                    self.lila_syls.remove(syl)
        self.deletedlist = self.spieler.appendlist[:]
        self.spieler.appendlist = []

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
        self.screen_copy.fill(self.gray, (0, 0, self.screenw,self.screenh))
        self.tript2.blit(self.hintergrund, (0, 0)) # der Hintergrund ist links dunkler als rechts und ergibt auf diese Weise Wände
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
        lil = self.lila_syls[:]
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
        code_tuples = [w.tuples for w in self.woerter.code_words]

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
        self.blit_clickable_words(text, self.white, (0, self.down), screen=surface)

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
        binary_list = {" NEU >>> ": " ALT>>>>"}
        self.screen_copy.blit(self.bigger_font.render(" ALT >>>> ", True, self.cyan), (0, digits_line))
        list_code_satz = self.woerter.code_satz.split()
        digit_identation = self.bigger_font.render(" ALT >>>> ", True, self.dark).get_rect().w

        the_calculation_result = []

        for i in range(len(list_code_satz)):  # füllt den Woerterbuch auf
            code_number_at_this_index = list(self.binary_code)[i]
            opposite = 0 if code_number_at_this_index == '1' else 1
            if i < len(
                    self.guessed_code_words):  # diese Klause umfasst die code-woerter die moeglicherweise erraten wurden
                dieses_code_wort = self.guessed_code_words[i].name
                space_nach_ziffer = self.bigger_font.render(f'{dieses_code_wort} ', True, self.dark).get_rect().w
                # print(dieses_code_wort,len(space_nach_ziffer))
                if dieses_code_wort == list_code_satz[i]:  # checkt, ob das richtige Wort im richtigen Platz ist
                    binary_list[
                        f'{dieses_code_wort}'] = f'{code_number_at_this_index}{"placeholder"}'  # wenn ja, ergibt die originelle Ziffer
                else:
                    binary_list[
                        f'{dieses_code_wort}'] = f'{opposite}{"placeholder"}'  # wenn nein, ändert 1 zum 0 oder 0 zum 1
                    code_number_at_this_index = opposite
            else:
                ziffer = f'{i + 1}'
                space_nach_ziffer = self.bigger_font.render(ziffer, True, self.dark).get_rect().w
                binary_list[ziffer] = f'{opposite} '  # die nicht-erratene woerter ergeben immer 0
                code_number_at_this_index = opposite

            the_calculation_result.append((code_number_at_this_index, digit_identation))

            digit_identation += space_nach_ziffer

        for (code_number, indentation) in the_calculation_result:
            self.screen_copy.blit(self.bigger_font.render(f'{code_number}',True,self.cyan), (indentation,digits_line))


        end_code_numbers = 2 * digits_line
        end_header = self.blit_clickable_words(
            [a for a in binary_list.keys() if a not in [str(b) for b in range(0, 1000)]], self.yellow,
            (self.screenw, end_code_numbers), no_buttons=False, start_end=(0, 100), afont=self.bigger_font)
        self.end_header = end_header
        self.top = self.end_header + self.space

    def check_num_buttons(self,
                          click):  # the buttons were made using coordinates starting from 0,0 in the screen given to blit_words()
        '''
        Prueft, ob auf einem Button-Objekt geclickt wurde. Wenn ja, speichert der Index von diesem Objekt
        in der Variabel "self.word_to_move"
        :param click: das Mausclick
        :return: None
        '''

        if self.buttons:  # self.buttons only refers to the guessed code words on trypt2
            click_rect = Rect(click[0], click[1], 1, 1)
            index = click_rect.collidelist([a.rect for a in self.buttons]) -1
            # das "-1" kompensiert dafür, dass der erste object im self.buttons ("NEU>>>") nicht berücksichtigt wird
            if index != -1 and index != -2: # "-2" bedeutet keine Kollision und "-1" bedeutet das nicht zu berücksichtigen element "NEU>>>"
                self.word_to_move = index
            else:
                self.word_to_move = None
                self.temp_update_code_defs = None
