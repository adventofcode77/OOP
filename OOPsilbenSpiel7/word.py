import pygame as pg
from pygame import *
from OOPsilbenSpiel7 import silbe
import globale_variablen

class Word(globale_variablen.Settings):
    def __init__(self, key, meaning,txtsilben):
        super().__init__()
        self.meaning = meaning.split(" ")
        print("word init",key,len(txtsilben),self.meaning)
        self.name = key
        self.txtsilben = txtsilben
        self.bits = self.get_bits()
        self.syls = self.make_silben() #[silbe.Silbe("it","word","def inition")] #[silbe.Silbe(a, self.name) for a in silben]
        self.image = self.font.render(self.name, False, self.black)
        self.rect = self.image.get_rect() # draw_rect()?
        self.rect.x = 0 #random.randrange(0,500-self.rect.w,50)

    def too_few_def_words(self,list,n):
        listoflists = []
        for i in range(len(list)):
            listoflists.append(list[i])
        return listoflists

    def get_bits(self):
        definition = self.meaning
        list_of_lists = []
        num_syls = 5
        advancement = len(definition)//num_syls
        if advancement == 0:
            advancement = 1
        for i in range(0,len(definition),advancement):
            if i+advancement*2 >= len(definition):
                list_of_lists.append(definition[i:])
                break
            else:
                list_of_lists.append(definition[i:(i+advancement)])
        return list_of_lists # DO NOT FORGET RETURN


    def make_silben(self):
        syls = []
        if len(self.txtsilben)>len(self.bits):
            smaller = len(self.bits)
            bigger = len(self.txtsilben)
        else:
            smaller = len(self.txtsilben)
            bigger = len(self.txtsilben)
        for i in range(smaller):
            print(i, self.bits)
            bit = self.bits[i] + [" "]
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it,word,bit)
            syls.append(silbe1)
            print(it, word, bit)
        for i in range(smaller,bigger):
            bit = "."
            it = self.txtsilben[i]
            word = self.name
            silbe1 = silbe.Silbe(it, word, bit)
            syls.append(silbe1)
            print(it,word,bit)
        return syls
