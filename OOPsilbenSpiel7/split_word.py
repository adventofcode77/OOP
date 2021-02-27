def split_word_syls(word): # german-specific #Angstschweiß
    word_syls = []
    divide_before = ["ch", "ck", "ph", "rh", "sh", "th", "sch"]
    divide_after = ["au", "eu", "ie", "ei", "äu"]
    vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
    attach_ks_front = True
    def split_ks(ks): # returns a tuple of an element to attach to previous part of hte word and one for the next part
        print("ks",ks)
        if len(ks) == 1:
            attach_ks_front = False
            return (None, ks) #attach nothing at front
        elif len(ks) == 2 and ks[0] == ks[1]:
            return (ks[0],ks[0])
        for elem in divide_before+divide_after:
            if elem in ks: #sch #rl
                index = ks.index(elem)
                if ks[:index]:
                    split_ks(ks[:index]) # ngst
                if ks[index:]:
                    split_ks() # w
            else:
                print("for elemm return",ks)
                return (ks[:-1],ks[-1:])
    #while True: # abitur #bitur #tur #kette
    encountered_vowel = False
    index_last_vowel = 0
    for i in range(len(word)): # Angstschweiß
        print("i is",i,"and len is",len(word),"and word is",word)
        char = word[i].lower()
        if char in vowels: #u
            if encountered_vowel:
                print("in encountered",char,index_last_vowel)
                encountered_vowel = False
                ks = word[index_last_vowel+1:i] #1:2=b #t
                print(ks)
                split = split_ks(ks) # b #t
                toappend = word[:index_last_vowel+1]
                if split and split[0] is not None:
                    toappend += split[0]
                word_syls.append(toappend) #a #bi
                word = word[i:]
                if split and split[1] is not None:
                    word = split[1] + word
                return word_syls + split_word_syls(word)
            else:
                encountered_vowel = True
            index_last_vowel = i
        if i == len(word)-1:
            word_syls.append(word) #tur
            return word_syls
        else:
            print(i,len(word)-1, char, word_syls)


print(split_word_syls("Angstschweiß"))
