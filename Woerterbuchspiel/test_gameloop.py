from unittest import TestCase
import logging, pickle, pygame
import gameloop, woerterbuch


class GameMainTest(TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    with open('testlog', 'a') as f:
        f.write("Texten,")

    def setUp(self):
        pygame.init()
        file_paths = [
            '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml']  # XML FILE AUS WIKTIONARY https://dumps.wikimedia.org/dewiktionary/20210501/
        code_satz = ["Das Herz der verliebten Dame schlägt für den Bauern"]  # CODE SATZ
        letztes_spiel_code = "000011001"
        woerterbuch_objekt = woerterbuch.Woerterbuch(file_paths[0])
        with open('Woerterbuchspiel/die_erste_1000_word_lists.txt', 'rb') as handle:
            data = handle.read()
        die_erste_1000_word_lists = pickle.loads(data)
        spielwoerter = woerterbuch_objekt.quick_get(50, list_of_word_lists=die_erste_1000_word_lists)
        try:
            self.test_gameloop = gameloop.Gameloop(code_satz, file_paths, letztes_spiel_code, spielwoerter)
            # test_gameloop.main_loop = True
            # test_gameloop.wait = True
            self.test_gameloop.mainloop()
        except:
            self.logger.info("could not make gameloop and mainloop")

    def testGameMain(self):
        self.logger.info("start logging")
        try:
            self.assertEqual(self.test_gameloop.info.next_counter,0,"nextcounter == 0")
            self.test_gameloop.info.next_counter = 1
            self.test_gameloop.info.menu.testcounter =
            self.assert

        except:
            self.logger.info("assert next counter did not run")
        finally:
            print("Ende Testing")

