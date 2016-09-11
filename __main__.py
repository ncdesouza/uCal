from ucal import UCal
from gui import GUI

def main():
    ucal = UCal()
    gui = GUI(ucal.start, ucal.clear_all)
    gui.master.title('uCal - Import your UOIT schedule to google calendar')
    gui.mainloop()


if __name__ == '__main__':
    main()