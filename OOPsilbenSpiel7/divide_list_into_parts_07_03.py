def get_bits(self,alist, num_parts): #goal: divide a list into roughly equal parts such that no part is empty
        list_of_lists = []
        while len(alist) < num_parts:
            alist += ["..."]
        advancement = (len(alist) // num_parts)
        if advancement == 0:
            advancement = 1
        while alist:
            if len(alist) < advancement or len(list_of_lists) >= num_parts-1:
                list_of_lists.append(alist)
                alist = []
            else:
                list_of_lists.append(alist[:advancement])
                alist = alist[advancement:]
        if len(list_of_lists) > num_parts:
            print("get_bits() outputs more list parts than the parameter specifies")
            quit()
        return list_of_lists # DO NOT FORGET RETURN

list = ['Wir', 'entdecken', 'einen', 'PC,', 'der', 'anscheinend', 'einen', 'Countdown', 'anzeigt,', 'ein', 'anderer', 'PC', 'fordert', 'uns', 'zur', 'Eingabe', 'eines', 'Codes', 'auf.Nur', 'welchen?', 'Auf', 'einem', 'Computer', 'erscheint', 'nur', 'die', 'Shell...', 'Daneben', 'finden', 'wir', 'einen', 'Zettel', 'mit', 'der', 'Aufschrift', "'Help'.Mit", 'unwohlen', 'Gefühlen', 'betrachte', 'ich', 'all', 'das', 'was', 'mir', 'gerade', 'die', 'Sinne', 'raubt.Jedes', 'Level,jeder', 'Code', 'hilft', 'beim', 'Weiterkommen', 'und', 'Auffinden', 'der', 'Hinweise', 'für', 'die', 'Codes,', 'um', 'zum', 'nächsten', 'Rätsel', 'zu', 'gelangen.Diese', 'Software', 'gibt', 'Hinweise,', 'den', 'Code', 'zu', 'knacken.', 'Der', 'Code,', 'den', 'man', 'mit', 'dem', 'letzten', 'Hinweis', 'findet,', 'öffnet', 'die', 'Tür.Der', 'Countdown', 'läuft', 'eine', 'Stunde.', 'Wenn', 'Sie', 'es', 'nicht', 'schaffen', 'innerhalb', 'dieser', 'Stunde', 'den', 'Code', 'oder', 'die', 'Rätsel', 'zu', 'knacken,dann', 'wird', 'der', 'Strom', 'ausfallen,', 'weil', 'eine', 'Strahlenkanone', 'zu', 'feuern', 'startet', 'und', 'somit', 'die', 'totale', 'unaufhaltsameVerpixelung', 'aller', 'Lebewesen', 'durch', 'die', 'KI', 'beginnt.', 'Sie', 'haben', 'eine', 'Stunde', 'Zeit,', 'um', 'aus', 'diesem', 'Raum', 'zu', 'entkommenund', 'die', 'Erde', 'zu', 'retten.', 'Viel', 'Glück!']
print(get_bits(list,14))
print(get_bits([''],3))
