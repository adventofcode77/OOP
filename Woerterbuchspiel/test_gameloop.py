from unittest import TestCase
import logging, pickle, pygame
from Woerterbuchspiel import gameloop, woerterbuch, game, globale_variablen

class TestGameloop(TestCase):
    def setUp(self):
        from datetime import datetime
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        self.globale_variablen = globale_variablen.Settings()
        self.font = self.globale_variablen.default_font
        file_paths = [
            '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml']  # XML FILE AUS WIKTIONARY https://dumps.wikimedia.org/dewiktionary/20210501/
        code_satz = ["Das Herz der Dame im Turm schlägt für den Bauern"]  # CODE SATZ
        letztes_spiel_code = "0000011001"
        woerterbuch_objekt = woerterbuch.Woerterbuch(file_paths[0])

        with open('1000_word_lists.txt', 'rb') as handle:
            data = handle.read()
        die_ersten_1000_word_lists = pickle.loads(data)

        spielwoerter = woerterbuch_objekt.quick_get(50, list_of_word_lists=die_ersten_1000_word_lists)

        self.gameloop_ = gameloop.Gameloop(code_satz, file_paths, letztes_spiel_code, spielwoerter)
        #self.gameloop_.mainloop() # starts the game and upon closing it the needed modules are again unitiated

    def append_to_testlog(self,message):
        with open('testlog', 'a') as self.f:
            self.f.write(f'{self.current_time} \n')
            self.f.write(f'{message} \n')

    def reset_testlog(self):
        open('testlog', 'w').close()

    def test_mainloop_wait_is_initially_false(self):
        self.append_to_testlog(" in test_mainloop_wait_is_initially_false")
        assert self.gameloop_.wait == False

    def test_negative_time_left_changes_lost_to_true(self):
        self.append_to_testlog("in test_negative_time_left_changes_lost_to_true \n")
        self.gameloop_.check_time_left(-1)
        assert self.gameloop_.lost == True
        assert self.gameloop_.wait == True

'''
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
        with open('Woerterbuchspiel/erste_1000_word_lists.txt', 'rb') as handle:
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
            self.assertEqual(self.test_gameloop.info.next_counter, 0, "nextcounter == 0")
            self.test_gameloop.info.next_counter = 1
            self.test_gameloop.info.menu.testcounter =
            self.
            assert

            except:
            self.logger.info("assert next counter did not run")
        finally:
            print("Ende Testing")
'''



