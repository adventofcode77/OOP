from Woerterbuchspiel import silbe




class Word():
    '''
    Diese Klasse erzeugt Wort-Objekte
    '''
    all_syls = []

    def __init__(self, key, meaning,txtsilben,worder,totalsyls,info,color=None):
        self.info = info
        self.totalsyls = totalsyls

        self.worder = worder
        self.name = key
        self.meaning = meaning.split()
        for i in range(len(self.meaning)):
            if not self.meaning[i]:
                self.meaning.insert(i,"...")
        self.txtsilben = txtsilben
        Word.all_syls.append(txtsilben)
        self.bits = self.info.get_bits(self.meaning, len(self.txtsilben))
        self.syls = self.make_silben(self.info.make_rgb())
        self.image = self.info.default_font.render(self.name, True, self.info.gold)
        self.rect = self.image.get_rect() # draw_rect()?
        self.color = color
        self.tuples = [s.tuple for s in self.syls]
        self.is_code_word = False
        self.is_guessed = False
        self.name_from_syls = " ".join([syl.name for syl in self.syls])

    def make_blank_word(self):
        return Word("", "", [], 404, 404, self.info)


    def update(self):
        self.name_from_syls = "".join([syl.name for syl in self.syls])
        self.bits = [syl.bit for syl in self.syls]
        self.tuples = [s.tuple for s in self.syls]
        self.meaning = [word for bit in self.bits for word in bit]
        print("type word meaning",self.meaning)

    def make_silben(self, rgb):
        syls = []
        for i in range(len(self.txtsilben)):
            it = self.txtsilben[i]
            if i < len(self.bits):
                bit = self.bits[i]
            else:
                bit = [...]
            word = self.name
            silbe1 = silbe.Silbe(it, word, bit, self.totalsyls, self.worder, self.info, rgb)
            syls.append(silbe1)
            self.totalsyls += 1
        return syls

class Button():
    '''
        Diese Klasse erzeugt Button-Objekte
        '''
    def __init__(self, word_string,word_img,word_rect,word_index):
        self.text = word_string
        self.img = word_img
        self.rect = word_rect
        self.index = word_index

