def split_word_syls(word): # german-specific #Angstschweiß
    word = word.lower()
    word_syls = []
    divide_before_with_priority = ['sch']
    divide_before = ["ck", "ph", "rh", "sh", "th", "bl","cl","fl","gl","pl","tl"]
    divide_after = ["au", "eu", "ie", "ei", "äu","ch"] #lc?
    vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü"]
    def split_ks(ks): # returns a tuple of an element to attach to previous part of hte word and one for the next part
        print("ks",ks)
        if len(ks) == 1:
            return (None, ks) #attach nothing at front
        elif len(ks) == 2 and ks[0] == ks[1]:
            return (ks[0],ks[0])
        for elem in divide_before_with_priority:
            if elem in ks:
                this_index = ks.index(elem)
                return (ks[:this_index],ks[this_index:])
        for elem in divide_before:
            if elem in ks: #sch #rl
                this_index = ks.index(elem)
                return (ks[:this_index],ks[this_index:])
        for elem in divide_after:
            print("divide after loop")
            if elem in ks:
                print("does ei land here")
                this_index = ks.index(elem)
                return (ks[:this_index+len(elem)],ks[this_index+len(elem):])
        print("no nonsplittable",ks)
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
                    print("any in",word[i+1:i+3],"for word",word)
                    if any(el in word[i+1:i+3] for el in divide_after):
                        print("any is true")
                        rest_word = word[i+1:]
                        for j in range(len(rest_word)):
                            if rest_word[j] in vowels:
                                ks = split_ks(rest_word[:j])
                                print("ks for special case",ks)
                                toappend += ks[0] # try: attach (els from divide_after+next ks) to undividable vowel pairs
                                next_part = ks[1] + rest_word[j:]
                                word_syls.append(toappend)

                    else:
                        print("in the first else?")
                        if i+1 == len(word)-1:
                            word_syls.append(toappend) #a #bi
                            next_part = None
                            if word_syls:
                                print("word syls exists?")
                                word_syls[-1] += word[i+1]
                            else:
                                word_syls = [word[i+1]]

                        else:
                            next_part = word[i+1:]
                            if split and split[1] is not None:
                                next_part = split[1] + word[i+1:]
                            word_syls.append(toappend) #a #bi
                    if next_part:
                        return word_syls + split_word_syls(next_part)
                    else:
                        return word_syls

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
                    print("LEN",len(next_part))
                    if len(next_part)==1:
                        if word_syls:
                            word_syls[-1] += word
                        else:
                            word_syls = [word]
                        return word_syls
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
            else:
                print("are you here?")
                word_syls = [word]
            return word_syls

def split_string_into_syls(string):
    string = string.split()
    all_syls = []
    for word in string:
        all_syls.append(split_word_syls(word))
    return all_syls


print(split_string_into_syls("milchig"))
