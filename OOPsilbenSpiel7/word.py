import pygame as pg
from pygame import *
from OOPsilbenSpiel7 import silbe
from OOPsilbenSpiel7 import spieler
import globale_variablen

class Word(globale_variablen.Settings):
    def __init__(self, key, meaning,txtsilben):
        super().__init__()
        self.spieler = spieler.Spieler()
        self.meaning = meaning.split(" ")
        self.name = key
        self.txtsilben = txtsilben
        self.bits = self.get_bits()
        self.syls = self.make_silben() #[silbe.Silbe("it","word","def inition")] #[silbe.Silbe(a, self.name) for a in silben]
        self.image = self.font.render(self.name, False, self.spieler.black)
        self.rect = self.image.get_rect() # draw_rect()?
        self.rect.x = 0 #random.randrange(0,500-self.rect.w,50)

    def too_few_def_words(self,list,n):
        listoflists = []
        for i in range(len(list)):
            listoflists.append(list[i])
        return listoflists

    def divide(self,list, n):
        listoflists = []
        if n == 0:
            listoflists = self.too_few_def_words(list,n)
            #print(listoflists)
            return 0
        for i in range(0,len(list),n): # range(6) is not the values of 0 to 6, but 0 to 5.
            current_part = i+n
            if current_part+n>len(list):
                listoflists.append(list[i:])
            else:
                listoflists.append(list[i:current_part])
        #print(listoflists)
        return listoflists #missing return makes chaining methods fail

    def get_bits(self):
        listdef = self.meaning # 2 elements
        n_el_in_each_part = len(self.meaning)//len(self.txtsilben) #exactly correct
        if n_el_in_each_part == 0:
            n_el_in_each_part = 1
        return self.divide(listdef,n_el_in_each_part)

    def get_bits_no_more(self):
        #print("word:",self.name)
        #print("syls",self.txtsilben)
        #print("meaning:",self.meaning)
        array = [None]*len(self.txtsilben) #[[]*x] gave an empty array
        #print("length of txtsilben:",len(self.txtsilben)," length of array:",len(array))
        arrayindexcounter = 0
        sizeofeachchunk = len(self.meaning)//len(self.txtsilben)
        if sizeofeachchunk == 0:
            sizeofeachchunk = 1
        #print("size of each chunk",sizeofeachchunk)
        for i in range(0,len(self.meaning)-1,sizeofeachchunk):
            #print("counter:",arrayindexcounter," length of array:", len(array))
            #print("i:",i)
            if i+sizeofeachchunk>len(self.meaning):
                toappend = self.meaning[i:]
            else:
                toappend = self.meaning[i:(i+sizeofeachchunk)]
                #print("array element at counter:",array[arrayindexcounter])
                if len(toappend) == 0:
                    array[arrayindexcounter] = self.meaning[i]
                    #print("list to append to array:",self.meaning[i])
                else:
                    array[arrayindexcounter] = toappend
                    #print("list to append to array:",i,":",toappend)
            arrayindexcounter += 1
        #print("return array:",array)
        return array

    def make_silben(self):
        syls = []
        for i in range(len(self.txtsilben)-1):
            it = self.txtsilben[i]
            word = self.name
            if i >= len(self.bits):
                bit = ""
            else:
                bit = self.bits[i]
                if isinstance(bit, list):
                    bit = bit[0]
            silbe1 = silbe.Silbe(it,word,bit)
            syls.append(silbe1)

        return syls
