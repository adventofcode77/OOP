import pygame as pg
import random
from OOPsilbenSpiel7 import woerterbuch
from OOPsilbenSpiel7 import word
from OOPsilbenSpiel7 import silbe
import random

class Woerter():
    all_syls = []
    def __init__(self, game_instance):
        self.info = game_instance
        self.dictwithkeyname = self.get_bank()
        self.totalsyls = 0
        self.worder = 0
        self.words = self.get_words(self.dictwithkeyname)
        self.silben = self.get_silben()
        self.num_syls = self.get_num_code_syls(self.info.input_code)
        self.placeholder_code_text = self.get_escape_game_text()
        self.code_word_text_bits = self.info.get_bits(self.placeholder_code_text.split(), len(self.info.input_code.split()))
        self.code_words = []
        self.code_syls = []
        self.get_code_words_and_syls(self.info.input_code)

    def get_num_code_syls(self, input_code):
        num_syls = 0
        words = input_code.split()
        for word in words:
            num_syls += len(self.split_word_syls(word))
        return num_syls

    def get_escape_game_text(self):
        with open('escape_game_text', 'r') as file:
            # "with" takes care of closing the file # replace absolute paths with relative?
            text = file.read().replace('\n', ' ')
        return text

    def get_bank(self):
        parser = woerterbuch.Woerterbuch(self.info.file_path, self.info.language)
        return parser.parsed

    def get_words(self,source):
        words = []
        for entry in source:
            self.worder += 1
            name = entry
            meaning = source[entry][0]
            syls = source[entry][1]
            Woerter.all_syls.append([syl for syl in syls])
            aword = word.Word(name, meaning, syls, self.worder, self.totalsyls, self.info)
            words.append(aword)
            self.totalsyls += len(syls)
        return words

    def get_silben(self):
        sylobjects = []
        for aword in self.words:
            for asyl in aword.syls:
                sylobjects.append(asyl)
        return sylobjects

    def get_code_words_and_syls(self, string): # https://www.sttmedia.com/syllablefrequency-german
        words = string.split()
        bits_counter = 0
        for i in range(len(words)):
            self.worder += 1
            aword = words[i]
            syls = self.split_word_syls(aword)
            len_syls = len(syls)
            word_bit_string = " ".join(self.code_word_text_bits[i])
            word_object = word.Word(aword, word_bit_string, syls, self.worder, self.totalsyls, self.info)
            self.code_words.append(word_object)
            bits_counter += len_syls
        for aword in self.code_words: # can't say "for word in" because of word.Word
            self.code_syls.append(aword.make_silben(self.info.make_rgb()))
        self.code_syls = [elem for list in self.code_syls for elem in list]

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
                    if next_part:
                        return word_syls + self.split_word_syls(next_part)
                    else:
                        return word_syls
                else:
                    encountered_vowel = True
                index_last_vowel = i
            if i == len(word)-1:
                if word_syls:
                    word_syls[-1] += word
                else:
                    word_syls = [word]
                return word_syls











