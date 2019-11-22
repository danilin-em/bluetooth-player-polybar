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


def find_player_path(pattern=None):
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                             "org.freedesktop.DBus.ObjectManager")
    objects = manager.GetManagedObjects()
    for path, _ in objects.items():
        if path.endswith('player0'):
            return path
    raise Exception("Bluetooth adapter not found")


class AppExeption(Exception):
    """ App Exeption """


class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    """ Catch Errors in argparse """
    def error(self, message):
        raise AppExeption(message)


class Player:
    """ Player DBus Wrapper """
    dbus_interface_path = 'org.bluez.MediaPlayer1'
    dbus_properties_path = 'org.freedesktop.DBus.Properties'

    def __init__(self, path=None):
        path = find_player_path()
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        self.bluez = bus.get_object('org.bluez', path)
        self.iface = dbus.Interface(self.bluez,
                                    dbus_interface=self.dbus_interface_path)

    def get_props(self):
        dbus_properties_iface = dbus.Interface(
            self.bluez, dbus_interface=self.dbus_properties_path)
        prop = dbus_properties_iface.GetAll(self.dbus_interface_path)
        return prop


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
        help='Player path')

    parser.add_argument(
        'action',
        type=str,
        choices=actions_names,
        help='app actions')
    try:
        args = parser.parse_args(argv)
    except AppExeption as error:
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
        status = '> {} {} — {}'.format(prop['Status'], prop['Track']['Artist'], prop['Track']['Title'])
        print(status)
        return status

    def action_play(self):
        """ Player: play """
        return self.player.iface.Play()

    def action_pause(self):
        """ Player: pause """
        return self.player.iface.Pause()

    def action_stop(self):
        """ Player: stop """
        return self.player.iface.Stop()

    def action_next(self):
        """ Player: next """
        return self.player.iface.Next()

    def action_previous(self):
        """ Player: previous """
        return self.player.iface.Previous()


def main(argv):
    """ Main """
    args = cli(argv)
    if not args:
        return False
    pl = Player(args.p)
    act = Actions(pl)
    return act.exec(args.action)


if __name__ == '__main__':
    main(sys.argv[1:])
