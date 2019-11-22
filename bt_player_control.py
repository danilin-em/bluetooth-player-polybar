"""Bluetooth Player Control

@author Evgenii Danilin <evgenii.danilin.m@gmail.com

"""
import sys
import argparse


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    """ Catch Errors in argparse """
    def error(self, message):
        raise ValueError(message)


class CliIface():
    """ Cli Interface """
    actions = {}
    parser = ErrorRaisingArgumentParser(
        description='Bluetooth Player Control')

    def __init__(self):
        self.parser.add_argument(
            '-s',
            type=str,
            help='Some arg')

    def parse(self, argv):
        """ Parse args """
        actions_keys = self.actions.keys()
        self.parser.add_argument(
            'action',
            type=str,
            choices=actions_keys,
            help='app actions')
        args = self.parser.parse_args(argv)
        return args

    def action(self, func):
        """ Add Action """
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        _, name = func.__name__.split('_', 1)
        self.actions[name] = wrapper
        return wrapper

    def exec(self, action):
        """ Execute action by Name """
        if action in self.actions:
            return self.actions[action]()
        raise 'Unknown action'


CLI = CliIface()


@CLI.action
def app_status():
    """ Get Status line """
    print('Some song...')
    return 'status'


@CLI.action
def player_play():
    """ Player: play """
    return 'play'


@CLI.action
def player_pause():
    """ Player: pause """
    return 'pause'


@CLI.action
def player_stop():
    """ Player: stop """
    return 'stop'


@CLI.action
def player_next():
    """ Player: next """
    return 'next'


@CLI.action
def player_previous():
    """ Player: previous """
    return 'previous'


def main(argv):
    """ Main """
    args = CLI.parse(argv)
    return CLI.exec(args.action)


if __name__ == '__main__':
    main(sys.argv[1:])
