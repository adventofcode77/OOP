from unittest import TestCase
import game


class TestGame(TestCase):
    def test_get_syl_returns_None(self):
        syl = game.Game.get_syl(0, 0, [], 10)
        assert syl is None

    def test_get_syl_returns_element_0(self):
        syl = game.Game.get_syl(0, 0, [2,3], 1)
        assert syl == 2

    def test_get_syl_returns_the_first_element_in_second_column(self):
        assert game.Game.get_syl(1, 0, [2, 3, 4, 5, 6], 3) == 5
        assert game.Game.get_syl(1, 1, [2, 3, 4, 5, 6], 3) == 6
        assert game.Game.get_syl(1, 2, [2, 3, 4, 5, 6], 3) is None

