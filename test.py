"""Tests

Base Unit Tests

"""

import unittest

import bt_player_polybar


class BaseTest(unittest.TestCase):
    """ Base Test """
    def test_main(self):
        """ Base Main Test """
        self.assertTrue(bt_player_polybar.main())


if __name__ == '__main__':
    unittest.main()
