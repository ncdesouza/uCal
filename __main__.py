from ucal import UCal
from gcal import GCal, Event
from gui import GUI

def main():
    ucal = UCal()
    gui = GUI(ucal.start)
    gui.master.title('uCal - Import your UOIT schedule to google calendar')
    gui.mainloop()


if __name__ == '__main__':
    main()