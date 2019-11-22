"""Bluetooth Player Control

@author Evgenii Danilin <evgenii.danilin.m@gmail.com

"""

import sys
import argparse

import dbus
import dbus.mainloop.glib

SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"


class AppArgumentParserException(Exception):
    """ App Argument Parser Exception """


class AppOfflineException(Exception):
    """ App Offline Exception """


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    """ Catch Errors in argparse """
    def error(self, message):
        raise AppArgumentParserException(message)


def find_player_path():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                             "org.freedesktop.DBus.ObjectManager")
    objects = manager.GetManagedObjects()
    for path, _ in objects.items():
        if path.endswith('player0'):
            return path
    raise AppOfflineException('Bluetooth adapter not found')


class Player:
    """ Player DBus Wrapper """
    offline = False
    dbus_interface_path = 'org.bluez.MediaPlayer1'
    dbus_properties_path = 'org.freedesktop.DBus.Properties'
    player_path = None
    status_format = '{status} {artist} — {title}'
    status_playing = '>'
    status_paused = '||'
    status_offline = 'X'

    def __init__(self, opt=None):
        if opt.status_format:
            self.status_format = opt.status_format
        if opt.status_playing:
            self.status_playing = opt.status_playing
        if opt.status_paused:
            self.status_paused = opt.status_paused
        if opt.status_offline:
            self.status_offline = opt.status_offline
        if opt.player_path:
            self.player_path = opt.status_paused
        try:
            self.player_path = find_player_path()
        except AppOfflineException:
            self.status_format = '{status}'
            self.offline = True
            return None
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        self.bluez = bus.get_object('org.bluez', self.player_path)
        self.iface = dbus.Interface(self.bluez,
                                    dbus_interface=self.dbus_interface_path)

    def get_props(self):
        try:
            dbus_properties_iface = dbus.Interface(
                self.bluez, dbus_interface=self.dbus_properties_path)
            prop = dbus_properties_iface.GetAll(self.dbus_interface_path)
        except Exception:
            return {
                'Status': 'offline',
                'Track': {
                    'Artist': None,
                    'Title': None,
                }
            }
        return prop

    def get_status_format(self, status=None):
        status_format = self.status_format
        if status == 'playing':
            status_format = status_format.replace('{status}', self.status_playing)
        elif status == 'paused':
            status_format = status_format.replace('{status}', self.status_paused)
        else:
            status_format = status_format.replace('{status}', self.status_offline)
        return status_format


def cli(argv):
    """ Cli Parser """
    actions_names = [
        'status',
        'play',
        'pause',
        'stop',
        'next',
        'previous',
    ]
    parser = ErrorRaisingArgumentParser(
        description='Bluetooth Player Control')
    parser.add_argument(
        '-p',
        type=str,
        dest='player_path',
        metavar='PATH',
        help='Player path')
    parser.add_argument(
        '-f',
        type=str,
        dest='status_format',
        metavar='FORMAT',
        help='Status format (see: https://pyformat.info/)')
    parser.add_argument(
        '--status-playing',
        type=str,
        metavar='SYMBOL',
        help='Status "playing" symbol')
    parser.add_argument(
        '--status-paused',
        type=str,
        metavar='SYMBOL',
        help='Status "playing" symbol')
    parser.add_argument(
        '--status-offline',
        type=str,
        metavar='SYMBOL',
        help='Status "Offline"')
    parser.add_argument(
        'action',
        type=str,
        choices=actions_names,
        help='app actions')
    try:
        args = parser.parse_args(argv)
    except AppArgumentParserException as error:
        print(error)
        return None
    return args


class Actions:
    """ App Actions """
    def __init__(self, player=None):
        self.player = player

    def exec(self, name='status'):
        """ Execute Action """
        name = 'action_%s' % name
        action = getattr(self, name, False)
        if not action:
            raise Exception('Unknown action: %s' % name)
        return action()

    def action_status(self):
        """ Get Status line """
        prop = self.player.get_props()
        status = self.player.get_status_format(
            status=prop['Status'])
        if not self.player.offline:
            status = status.format(
                artist=prop['Track']['Artist'],
                title=prop['Track']['Title'])
        print(status)
        return status

    def action_play(self):
        """ Player: play """
        if self.player.offline:
            return False
        return self.player.iface.Play()

    def action_pause(self):
        """ Player: pause """
        if self.player.offline:
            return False
        return self.player.iface.Pause()

    def action_stop(self):
        """ Player: stop """
        if self.player.offline:
            return False
        return self.player.iface.Stop()

    def action_next(self):
        """ Player: next """
        if self.player.offline:
            return False
        return self.player.iface.Next()

    def action_previous(self):
        """ Player: previous """
        if self.player.offline:
            return False
        return self.player.iface.Previous()


def main(argv):
    """ Main """
    args = cli(argv)
    if not args:
        return False
    pl = Player(args)
    act = Actions(pl)
    return act.exec(args.action)


if __name__ == '__main__':
    main(sys.argv[1:])
