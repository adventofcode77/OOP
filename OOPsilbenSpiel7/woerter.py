import pygame as pg
import random
from OOPsilbenSpiel7 import woerterbuch
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import silbe
import random

class Woerter():
    all_syls = []
    def __init__(self,game_instance, input_code):
        self.info = game_instance
        self.rect = pg.Rect(0,0,20,20)
        self.dictwithkeyname = self.get_bank()
        self.totalsyls = 0
        self.worder = 0
        self.words = self.get_words()
        self.silben = self.get_silben()
        self.code_syls_txt = [word for list in self.split_string_into_syls(input_code) for word in list]
        self.placeholder_code_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.".split()
        self.code_text_bits = self.info.get_bits(self.placeholder_code_text,len(self.code_syls_txt))
        self.code_syls = self.make_code_syls()

    def get_bank(self):
        parser = woerterbuch.Woerterbuch()
        return parser.parsed

    def get_words(self):
        words = []
        for entry in self.dictwithkeyname:
            self.worder += 1
            name = entry
            meaning = self.dictwithkeyname[entry][0]
            syls = self.dictwithkeyname[entry][1]
            Woerter.all_syls.append([syl for syl in syls])
            aword = word.Word(name, meaning, syls, self.worder, self.totalsyls, self.info)
            words.append(aword)
            self.totalsyls += len(syls)
        return words

    def make_code_syls(self):
        counter = 0 # replace with
        code_syls = []
        for syl in self.code_syls_txt:
            self.worder += 1
            print("code syl",syl)
            it = syl
            word = "winner"
            if counter >= len(self.code_text_bits)-1:
                bit = ["!"]
            else:
                bit = self.code_text_bits[counter]
            counter += 1
            info = self.info
            rgb = self.info.make_rgb()
            code_syls.append(silbe.Silbe(it,word,bit,self.worder,self.totalsyls, info, rgb))
            self.totalsyls += 1
        return code_syls

    def get_silben(self):
        sylobjects = []
        for aword in self.words:
            for asyl in aword.syls:
                sylobjects.append(asyl)
        return random.sample(sylobjects,len(sylobjects)) #sample returns new list

    def split_string_into_syls(self, string):
        string = string.split()
        all_syls = []
        for word in string:
            all_syls.append(self.split_word_syls(word))
        return all_syls

    def split_word_syls(self,word): # german-specific #Angstschweiß
        word_syls = []
        divide_before_with_priority = ['sch']
        divide_before = ["ck", "ph", "rh", "sh", "th", "bl","cl","fl","gl","pl","tl"]
        divide_after = ["au", "eu", "ie", "ei", "äu","ch"]
        vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
        def split_ks(ks): # returns a tuple of an element to attach to previous part of hte word and one for the next part
            if len(ks) == 1:
                return (None, ks) #attach nothing at front
            elif len(ks) == 2 and ks[0] == ks[1]:
                return (ks[0],ks[0])
            for elem in divide_before_with_priority:
                if elem in ks:
                    this_index = ks.index(elem)
                    return (ks[:this_index],ks[this_index:])
            for elem in divide_before:
                if elem in ks:
                    this_index = ks.index(elem)
                    return (ks[:this_index],ks[this_index:])
            for elem in divide_after:
                if elem in ks:
                    this_index = ks.index(elem)
                    return (ks[:this_index+len(elem)],ks[this_index+len(elem):])
            return (ks[:-1],ks[-1:])
        encountered_vowel = False
        index_last_vowel = 0
        for i in range(len(word)):
            char = word[i].lower()
            if char in vowels: #u
                if encountered_vowel:
                    encountered_vowel = False
                    if index_last_vowel+1 == i:
                        ks = word[index_last_vowel:i+1]
                        split = split_ks(ks)
                        toappend = word[:index_last_vowel]
                        if split and split[0] is not None:
                            toappend += split[0]
                        if any(el in word[i+1:i+3] for el in divide_after):
                            rest_word = word[i+1:]
                            for j in range(len(rest_word)):
                                if rest_word[j] in vowels:
                                    ks = split_ks(rest_word[:j])
                                    toappend += ks[0] # try: attach (els from divide_after+next ks) to undividable vowel pairs
                                    next_part = ks[1] + rest_word[j:]
                                    word_syls.append(toappend)
                                    return word_syls + self.split_word_syls(next_part)
                        else:
                            next_part = word[i+1:]
                            if split and split[1] is not None:
                                next_part = split[1] + word[i+1:]
                        word_syls.append(toappend) #a #bi
                    else:
                        ks = word[index_last_vowel+1:i] #1:2=b #t
                        split = split_ks(ks) # b #t
                        toappend = word[:index_last_vowel+1]
                        if split and split[0] is not None:
                            toappend += split[0]
                        word_syls.append(toappend) #a #bi
                        next_part = word[i:]
                        if split and split[1] is not None:
                            next_part = split[1] + word[i:]
                    return word_syls + self.split_word_syls(next_part)
                else:
                    encountered_vowel = True
                index_last_vowel = i
            if i == len(word)-1:
                if word_syls:
                    word_syls[-1] += word
                else:
                    word_syls = [word]
                return word_syls











