from unittest import TestCase
import game


class TestGame(TestCase):
    def test_get_syl_returns_None(self):
        syl = game.Game.get_syl(0, 0, [], 10)
        assert syl is None
