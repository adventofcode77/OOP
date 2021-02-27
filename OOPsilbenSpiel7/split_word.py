def split_word_syls(word): # german-specific #Angstschweiß
    word_syls = []
    divide_before = ["ch", "ck", "ph", "rh", "sh", "th", "sch", "bl","cl","fl","gl","pl","tl"]
    divide_after = ["au", "eu", "ie", "ei", "äu"]
    vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
    def split_ks(ks): # returns a tuple of an element to attach to previous part of hte word and one for the next part
        print("ks",ks)
        first_index = 999
        first_nonsplittable = ""
        nonsplittable = False
        if len(ks) == 1:
            attach_ks_front = False
            return (None, ks) #attach nothing at front
        elif len(ks) == 2 and ks[0] == ks[1]:
            return (ks[0],ks[0])
        for elem in divide_before+divide_after:
            if elem in ks: #sch #rl
                nonsplittable = True
                this_index = ks.index(elem)
                print("this index is", this_index, "first index is", first_index)
                if this_index < first_index:
                    first_index = this_index # to get the first occurence of something nonsplittable
                    print("first index is", first_index)
                    first_nonsplittable = elem
                print("this_index",this_index,"of elem",elem,"first index is", first_index)
        if nonsplittable:
            nonsplittable = False
            print("nonsplittable; first_nonspl is", first_nonsplittable)
            if first_nonsplittable in divide_before:
                print("elem is in divide before")
                return (ks[:first_index],ks[first_index:])
            else:
                print("elem is in divide after")
                return (ks[first_index:],ks[:first_index])
        print("elem is in split ks bottom",ks)
        return (ks[:-1],ks[-1:])
    #while True: # abitur #bitur #tur #kette
    encountered_vowel = False
    index_last_vowel = 0
    for i in range(len(word)): # Angstschweiß # schweiß
        print("i is",i,"and len is",len(word),"and word is",word)
        char = word[i].lower()
        if char in vowels: #u
            if encountered_vowel:
                print("in encountered",char,index_last_vowel)
                encountered_vowel = False
                if index_last_vowel+1 == i:
                    ks = word[index_last_vowel:i+1]
                    split = split_ks(ks)
                    toappend = word[:index_last_vowel]
                    if split and split[0] is not None:
                        toappend += split[0]
                    print("toappend is",toappend)
                    word_syls.append(toappend) #a #bi
                    next_part = word[i+1:]
                    if split and split[1] is not None:
                        next_part = split[1] + word[i+1:]
                else:
                    ks = word[index_last_vowel+1:i] #1:2=b #t
                    print("ks",ks)
                    split = split_ks(ks) # b #t
                    print("split",split)
                    toappend = word[:index_last_vowel+1]
                    if split and split[0] is not None:
                        toappend += split[0]
                    word_syls.append(toappend) #a #bi
                    next_part = word[i:]
                    if split and split[1] is not None:
                        next_part = split[1] + word[i:]
                # if i == len(word)-1:
                #     print("do you go here")
                #     word_syls[-1] += next_part
                #     return word_syls
                # else:
                #     print("here",i,word)
                print("about to return word syls and func(nextpart).word syls is:",word_syls,"and next part is",next_part)
                return word_syls + split_word_syls(next_part)

            else:
                encountered_vowel = True
            index_last_vowel = i
        else:
            print("bottom",i,len(word)-1, char, word_syls)
        if i == len(word)-1:
            if word_syls:
                word_syls[-1] += word
                return word_syls
            else:
                word_syls = [word]
                return word_syls


print(split_word_syls("nächtsschnellere"))
