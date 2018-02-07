import json
import sys

import os

from ucal import UCal
from gui import GUI


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    ucal = UCal()

    try:
        with open(resource_path('save.json'), 'r') as f:
            credentials = json.load(f)
    except IOError:
        credentials = {'username': None, 'password': None}

    gui = GUI(ucal.start, ucal.clear_all, credentials['username'], credentials['password'])
    gui.master.title('uCal - Import your UOIT schedule to google calendar')
    gui.mainloop()


if __name__ == '__main__':
    main()
