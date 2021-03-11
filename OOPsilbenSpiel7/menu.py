import pygame as pg
from pygame import *
from pygame.locals import *
import math

class Menu():
    def __init__(self, game_instance):
        self.info = game_instance
        self.surface_cut = pg.Surface.subsurface(self.info.large_surface,pg.Rect(2000,0,3000,3000))
        self.offset = 0
        self.text_pos = (self.info.midtop[0], self.info.midtop[1] + self.offset + self.info.space)
        # keys
        self.verification_window = "V"
        self.workspace_window = "SPACE"
        self.cheating = "C"
        self.main_loop = "S"
        self.drop_objects = 2
        self.next, self.back = "DOWN", "UP"
        self.accelerate,self.deccelerate = "PLUS","MINUS"
        self.instructions = "I"

        start = f"Welcome to the Game Tutorial! Press {self.next} to Continue or {self.back} to go Back. To skip the tutorial, press {self.main_loop}."
        goal = f"The goal of this game is to assemble a secret code. The code is in the form of a sentence. " \
                   "To find the code, first collect objects. The objects that make up a word all have the same color." \
               "You need to collect them them in the right order to form a word. After you have all the code words, " \
               "put them in the right order to form the code sentence."
        move = f"To move, use the arrows or the ASWD keys. To change your speed, press {self.accelerate} or {self.deccelerate}." \
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
        self.instructions = [start, goal, move,pick,word_composing,code_word_composing,word_guessing,verify_code,cheating, game_window]
        for i in range(len(self.instructions)):
            liste = self.instructions[i].split()
            self.instructions[i] = liste

    def tutorial(self, next_counter):
        self.info.large_surface.fill(self.info.black)
        self.surface_cut.fill(self.info.black)
        if next_counter > len(self.instructions)-1:
            next_counter = 0
        elif next_counter < 0:
            next_counter = len(self.instructions)-1
        self.info.screen_copy.fill(self.info.black)
        blit_h = self.info.blit_string_words(self.instructions[next_counter],self.info.zuff,(self.info.midtop[0],self.info.midtop[1]+self.info.down*2),screen=self.surface_cut)
        self.info.text_wrap(self.info.screen_copy,self.info.large_surface,self.info.identation_surface_cut,blit_h)
        self.info.screen_transfer()
        return next_counter

    def overview(self): # all instructions in one window, then you can press a key to see the tutorial again
        pass



