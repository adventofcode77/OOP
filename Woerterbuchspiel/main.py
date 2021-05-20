import pygame as pg
import pickle

from Woerterbuchspiel import gameloop
from Woerterbuchspiel import woerterbuch


class Main:
    '''
    Diese Klasse startet das Spiel.
    '''

    #TODO ? make a script that downloads the wiktionary dump/imports the parser and configures their paths
    file_paths = ['/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'] # XML FILE AUS WIKTIONARY https://dumps.wikimedia.org/dewiktionary/20210501/
    code_satz = ["Das Herz der Dame im Turm schlägt für den Bauern"] # CODE SATZ
    letztes_spiel_code = "0000011001"
    woerterbuch_objekt = woerterbuch.Woerterbuch(file_paths[0])
    # spielwoerter = woerterbuch.Woerterbuch(file_paths[0]).quick_get(50) # SPIELWOERTER IN ACTIVE MODE

    ''' CODE FÜR PASSIVE MODE: Die folgenden linien erstellen eine Textdatei, die 
    die Funktion vom File woerterbuch.py ersetzt. Sie sind auskommentiert, weil die Textdatei
    (namens die_erste_1000_word_lists.txt) schon erstellt wurde.
    
    erste_1000_word_lists = woerterbuch_objekt.list_of_word_lists

    try:
        file = open('Woerterbuchspiel/die_erste_1000_word_lists.txt', 'wb')
        pickle.dump(erste_1000_word_lists, file)
        file.close()
    except:
        print("main.py records versuch gescheitert")

    '''

    with open('Woerterbuchspiel/die_erste_1000_word_lists.txt', 'rb') as handle:
        '''
        Hier wird die Textdatei aus dem Format XML zum Format Python (.py) umwandelt 
        und in der Variabel "spielwoerter" gespeichert.
        '''
        data = handle.read()
    die_erste_1000_word_lists = pickle.loads(data)

    spielwoerter = woerterbuch_objekt.quick_get(50, list_of_word_lists= die_erste_1000_word_lists)


    def __init__(self):
        '''
        Hier wird beim Aufrufen der Klasse Main die statishe Methode newgame() aufgerufen.
        '''
        self.newgame(Main.code_satz, Main.file_paths, Main.letztes_spiel_code, Main.spielwoerter)

    @staticmethod
    def newgame(code_satz, file_paths, letztes_spiel_code, spielwoerter):
        '''
        Hier wird ein Objekt aus der Klasse Gameloop erzeugt.
        Danach ruft dieses Objekt die mainloop() Methode, die das Spiel zum Laufen bringt.
        :param code_satz: Main.code_satz (Das Code-Satz, das die Aufgabe des Spielers ist, zu erraten)
        :param file_paths: Main.file_paths (Das ganze Woerterbuch im XML Format;
        wird momentan durch die variable "spielwoerter" ersaetzt)
        :param letztes_spiel_code: Main.letztes_spiel_code (Das uebernommene Code aus dem letzten Spiel)
        :param spielwoerter: Main.spielwoerter
        :return: None
        '''
        pg.init()
        #print(pg.font.get_fonts())
        gameloop_ = gameloop.Gameloop(code_satz, file_paths, letztes_spiel_code, spielwoerter)
        gameloop_.mainloop()
        print("Uebergabe Code:", gameloop_.game_objekt.output_code)

if __name__ == '__main__':
     Main()
