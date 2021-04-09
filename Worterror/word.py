import silbe

class Word():
    all_syls = []
    def __init__(self, key, meaning,txtsilben,worder,totalsyls,info,color=None):
        self.info = info
        self.totalsyls = totalsyls
        self.tuples = []
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

    def make_silben(self, rgb):
        syls = []
        for i in range(len(self.txtsilben)):
            it = self.txtsilben[i]
            if i < len(self.bits):
                bit = self.bits[i]
            else:
                bit = [...]
            word = self.name
            silbe1 = silbe.Silbe(it,word,bit,self.totalsyls, self.worder, self.info, rgb)
            syls.append(silbe1)
            self.tuples.append((self.totalsyls, self.worder))
            self.totalsyls += 1
        return syls

class Button():
    def __init__(self, word_string,word_img,word_rect,word_index):
        self.text = word_string
        self.img = word_img
        self.rect = word_rect
        self.index = word_index

