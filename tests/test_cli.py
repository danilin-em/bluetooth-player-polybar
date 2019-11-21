"""
Cli Interface Tests
"""

import unittest
import argparse

import bt_player_polybar


class CliIfaceTest(unittest.TestCase):
    """ Cli Interface Tests """
    def test_cli_parser(self):
        """ Try get status """
        action = 'status'
        cli = bt_player_polybar.CLI
        args = cli.parse([action])
        self.assertEqual(args, argparse.Namespace(action=action, s=None))

    def test_cli_parser_unknown_action(self):
        """ Pass invalid action """
        action = 'INVALID_ACTION'
        cli = bt_player_polybar.CLI
        self.assertRaises(ValueError, cli.parse, [action])

    # TODO app status
    # TODO player_play
    # TODO player_pause
    # TODO player_stop
    # TODO player_next
    # TODO player_previous


if __name__ == '__main__':
    unittest.main()
