list = [':[1]', 'Körperform']
syls = ['Fi', 'gur']
n = len(list)//len(syls)

#MAKE SILBEN EXECUTES. word: Mücke
# meaning: [':[1]', 'Gemeinde', ':w:Mücke', '(Gemeinde)|Mücke', 'im', 'Vogelbergskreis', 'in', 'Hessen']
# SYLLABLES! ['Mü', 'cke'] bits: None 0


def divide(list, n):
    listoflists = []
    if n == 0:
        listoflists = too_few_def_words(list,n)
        print(listoflists)
        return 0
    for i in range(0,len(list),n): # range(6) is not the values of 0 to 6, but 0 to 5.
        current_part = i+n
        if current_part+n>len(list):
            listoflists.append(list[i:])
        else:
            listoflists.append(list[i:current_part])
    print(listoflists)
    return listoflists

def too_few_def_words(list,n):
    listoflists = []
    for i in range(len(list)):
        listoflists.append(list[i])
    return listoflists

def get_bits():
        listdef = list # 2 elements
        n_el_in_each_part = len(list)//len(syls) #exactly correct
        if n_el_in_each_part == 0:
            n_el_in_each_part = 1
        return divide(listdef,n_el_in_each_part)

get_bits()
