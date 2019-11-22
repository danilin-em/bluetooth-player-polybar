"""
Cli Interface Tests
"""

import unittest
import argparse

import bt_player_control


class CliIfaceTest(unittest.TestCase):
    """ Cli Interface Tests """
    options = {
        'player_path': None,
        'status_format': None,
        'status_offline': None,
        'status_paused': None,
        'status_playing': None
    }

    def test_cli_parser(self):
        """ Try get status """
        action = 'status'
        args = bt_player_control.cli([action])
        self.assertEqual(args,
                         argparse.Namespace(action=action, **self.options))

    def test_cli_parser_unknown_action(self):
        """ Pass invalid action """
        action = 'INVALID_ACTION'
        args = bt_player_control.cli([action])
        self.assertEqual(args, None)

    # TODO app status
    # TODO player_play
    # TODO player_pause
    # TODO player_stop
    # TODO player_next
    # TODO player_previous


if __name__ == '__main__':
    unittest.main()
