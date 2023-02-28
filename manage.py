import sys

from server.utils import makemigrations
from server.runserver import initialize


commands = {
    'runserver': initialize,
    'migrate': makemigrations,
}


def available_commands():
    print('Available commands:')
    for command in commands:
        print(command)


def start():
    try:
        commands.get(sys.argv[1])()
    except IndexError:
        print('Required argument is missing.\n')
        available_commands()
    except TypeError:
        print('Invalid argument passed.\n')
        available_commands()


start()
