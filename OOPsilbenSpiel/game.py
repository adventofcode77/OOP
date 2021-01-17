import pygame, sys, time, random
import tkinter as tk
from tkinter.constants import *
from pygame.locals import *
from OOPsilbenSpiel import spieler
import numpy as np

class Game():
    def __init__(self):
        self.window = tk.Tk() #works
        self.datenbank = ["bei","spiel","bringen","platz"]
        self.user = spieler.Spieler()

    def show_bank(self):
        text_box = tk.Text()
        text_box.insert("1.0",self.datenbank)
        text_box.pack()
        tk.mainloop()




# if __name__ == '__main__':
#     pass

