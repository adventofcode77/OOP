import pygame as pg

from Woerterbuchspiel import gameloop
from Woerterbuchspiel import woerterbuch


class Main:
    #TODO ? make a script that downloads the wiktionary dump/imports the parser and configures their paths
    file_paths = ['/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'] # XML FILE AUS WIKTIONARY https://dumps.wikimedia.org/dewiktionary/20210501/
    code_satz = ["Das Herz der Verliebten Dame schlägt für den Bauern"] # CODE SATZ
    spielwoerter = woerterbuch.Woerterbuch(file_paths[0]).quick_get(50) # SPIELWOERTER
    letztes_spiel_code = "000011001"

    def __init__(self):
        self.newgame(Main.code_satz, Main.file_paths, Main.letztes_spiel_code, Main.spielwoerter)

    @staticmethod
    def newgame(code_satz, file_paths, letztes_spiel_code, dict):
        pg.init()
        #print(pg.font.get_fonts())
        gameloop_ = gameloop.Gameloop(code_satz, file_paths, letztes_spiel_code, dict)
        gameloop_.mainloop()
        # code = game1.output_code

if __name__ == '__main__':
     Main()
