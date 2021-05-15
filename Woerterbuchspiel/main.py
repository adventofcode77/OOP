import pygame as pg
import pickle

from Woerterbuchspiel import gameloop
from Woerterbuchspiel import woerterbuch


class Main:
    #TODO ? make a script that downloads the wiktionary dump/imports the parser and configures their paths
    file_paths = ['/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'] # XML FILE AUS WIKTIONARY https://dumps.wikimedia.org/dewiktionary/20210501/
    code_satz = ["Das Herz der verliebten Dame schlägt für den Bauern"] # CODE SATZ
    letztes_spiel_code = "000011001"
    woerterbuch_objekt = woerterbuch.Woerterbuch(file_paths[0])
    # spielwoerter = woerterbuch.Woerterbuch(file_paths[0]).quick_get(50) # SPIELWOERTER IN ACTIVE MODE

    ''' CODE FÜR PASSIVE MODE:
    erste_1000_word_lists = woerterbuch_objekt.list_of_word_lists

    try:
        file = open('Woerterbuchspiel/die_erste_1000_word_lists.txt', 'wb')
        pickle.dump(erste_1000_word_lists, file)
        file.close()
    except:
        print("main.py records versuch gescheitert")

    '''
    with open('Woerterbuchspiel/die_erste_1000_word_lists.txt', 'rb') as handle:
        data = handle.read()
    die_erste_1000_word_lists = pickle.loads(data)

    spielwoerter = woerterbuch_objekt.quick_get(50, list_of_word_lists= die_erste_1000_word_lists)


    def __init__(self):
        self.newgame(Main.code_satz, Main.file_paths, Main.letztes_spiel_code, Main.spielwoerter)

    @staticmethod
    def newgame(code_satz, file_paths, letztes_spiel_code, spielwoerter):
        pg.init()
        #print(pg.font.get_fonts())
        gameloop_ = gameloop.Gameloop(code_satz, file_paths, letztes_spiel_code, spielwoerter)
        gameloop_.mainloop()
        # code = game1.output_code

if __name__ == '__main__':
     Main()
