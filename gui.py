import Tkinter as tk
from tkFileDialog import asksaveasfilename
import datetime
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def center(window):
    window.update_idletasks()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    window.geometry("%dx%d+%d+%d" % (size + (x, y)))


class GUI(tk.Frame):
    def __init__(self, start_fnc, clear_fnc, username=None, password=None):
        master = tk.Tk()
        tk.Frame.__init__(self, master)
        self.start_fnc = start_fnc
        self.clear_fnc = clear_fnc

        self.username = tk.StringVar(self)
        self.valid_username = self.register(self.validate_username)
        self.username_status = tk.StringVar(self, 'Enter your MyCampus '
                                                  'Student ID')
        self.username_field = self.create_username_text_field()

        self.password = tk.StringVar(self)
        self.valid_password = self.register(self.validate_password)
        self.password_status = tk.StringVar(self, 'Enter your MyCampus '
                                                  'Password')
        self.password_field = self.create_password_text_field()
        self.save_credentials = tk.IntVar(self)
        self.save_credentials_checkbox = \
            self.create_save_credentials_checkbox()

        self.term_var = tk.IntVar()
        self.term_status = tk.StringVar(self, 'Select a Term')
        self.term_radio_buttons = self.create_term_radio_buttons()

        self.export_var = tk.IntVar()
        self.filepath = tk.StringVar(self, os.getcwd())
        self.file_opt = None
        self.file_labelframe = None
        self.export_labelframe = self.create_export_label_frame()

        self.reminders_labelframe = None
        self.color_var = tk.IntVar(self)
        self.room_var = tk.IntVar(self)
        self.location_var = tk.IntVar(self)
        self.privacy_var = tk.IntVar(self)
        self.availability_var = tk.IntVar(self)
        self.reminders_var = tk.IntVar(self)
        self.reminders_type = tk.IntVar(self)
        self.reminders_time = tk.StringVar(self, '5')
        self.optional_labelframe = self.create_optional_labelframe()

        self.start_button = self.create_start_button()
        self.quit_button = self.create_quit_button()
        self.options_button = self.create_options_button()

        if username and password:
            self.username_field[0].insert(tk.ANCHOR, username)
            self.password_field[0].insert(tk.ANCHOR, password)
            self.save_credentials.set(1)
            self.ready_to_start()

        self.check_term_status()

        self.grid()
        master.resizable(0, 0)
        center(master)

    def get_username(self):
        return self.username.get()

    def get_password(self):
        return self.password.get()

    def get_save_credentials(self):
        return self.save_credentials.get()

    def get_term(self):
        date = datetime.date.today()
        if self.term_var.get() == 1:
            if 5 <= date.month <= 12:
                year = date.year
            else:
                year = date.year - 1
            return str(year) + '09'

        else:
            if 1 <= date.month <= 4:
                year = date.year
            else:
                year = date.year + 1
            month = '01' if self.term_var.get() == 2 else '05'
            return str(year) + month

    def get_export_var(self):
        if self.export_var.get() == 1:
            return 'google calendar'
        elif self.export_var.get() == 2:
            return 'csv'
        elif self.export_var.get() == 3:
            return 'ics'

    def get_color_bool(self):
        return self.color_var.get()

    def get_room_bool(self):
        return self.room_var.get()

    def get_location_bool(self):
        return self.location_var.get()

    def get_privacy_bool(self):
        return self.privacy_var.get()

    def get_availability_bool(self):
        return self.privacy_var.get()

    def get_reminders_bool(self):
        return self.reminders_var.get()

    def get_reminders_type(self):
        if self.reminders_type.get() == 1:
            return 'email'
        elif self.reminders_type.get() == 2:
            return 'popup'

    def get_reminders_time(self):
        return self.reminders_time.get()

    def create_username_text_field(self):
        label = tk.Label(self, text='Username: ')
        txt = tk.Entry(self, bd=4, width=35,
                       textvariable=self.username,
                       validate='key',
                       validatecommand=(self.valid_username, '%P'))
        status = tk.Label(self, textvariable=self.username_status, fg='red',
                          width=30, anchor='w')

        label.grid(row=0, column=0, sticky=tk.E)
        txt.grid(columnspan=3, row=0, column=1, sticky=tk.W)
        status.grid(row=0, column=4)
        return txt, status

    def create_password_text_field(self):
        label = tk.Label(self, text='Password: ')
        txt = tk.Entry(self, show='*', bd=4, width=35,
                       textvariable=self.password,
                       validate='key',
                       validatecommand=(self.valid_password, '%P'))
        status = tk.Label(self, textvariable=self.password_status, fg='red',
                          width=30, anchor='w')

        label.grid(row=1, column=0, sticky=tk.E)
        txt.grid(columnspan=3, row=1, column=1, sticky=tk.W)
        status.grid(row=1, column=4)
        return txt, status

    def validate_username(self, value):
        if len(value) >= 9:
            self.username_status.set('Done')
            self.username_field[1]['fg'] = 'green'
        else:
            self.username_status.set('Enter your MyCampus Student ID')
            self.username_field[1]['fg'] = 'red'
        self.ready_to_start()
        return True

    def validate_password(self, value):
        if 6 <= len(value) <= 15:
            self.password_status.set('Done')
            self.password_field[1]['fg'] = 'green'
        else:
            self.password_status.set('Enter your MyCampus Password')
            self.password_field[1]['fg'] = 'red'
        self.ready_to_start()
        return True

    def create_save_credentials_checkbox(self):
        checkbox = tk.Checkbutton(self, text='Save Credentials',
                                  variable=self.save_credentials)
        checkbox.grid(columnspan=2, row=2, column=1, sticky=tk.W)
        return checkbox

    def create_term_radio_buttons(self):
        label = tk.Label(self, text='Term: ')
        fall_radio_btn = tk.Radiobutton(self, text='Fall',
                                        variable=self.term_var, value=1,
                                        command=self.validate_term)
        winter_radio_btn = tk.Radiobutton(self, text='Winter',
                                          variable=self.term_var, value=2,
                                          command=self.validate_term)
        summer_radio_btn = tk.Radiobutton(self, text='Summer',
                                          variable=self.term_var, value=3,
                                          command=self.validate_term)
        summer_radio_btn['state'] = tk.DISABLED
        status = tk.Label(self, textvariable=self.term_status, fg='red',
                          width=30, anchor='w')
        label.grid(row=3, column=0, sticky=tk.E)
        fall_radio_btn.grid(row=3, column=1)
        winter_radio_btn.grid(row=3, column=2)
        summer_radio_btn.grid(row=3, column=3)
        # status.grid(row=3, column=4)

        date = datetime.date.today()
        if 9 <= date.month <= 12:
            fall_radio_btn.select()
        elif 1 <= date.month <= 4:
            winter_radio_btn.select()
        elif 5 <= date.month <= 8:
            summer_radio_btn.select()

        return {'fall': fall_radio_btn,
                'winter': winter_radio_btn,
                'summer': summer_radio_btn}, status

    def check_term_status(self):
        if os.path.exists('events'):
            event_files = os.listdir(resource_path('events'))
            for ef in reversed(event_files):
                term = self.get_term()
                # print(ef[-11:-5], term, self.term_var.get())
                if ef[-11:-5] == term:
                    self.disable_term(self.term_var.get())

    def disable_term(self, term):
        if term == 1:
            self.term_radio_buttons[0]['fall']['state'] = tk.DISABLED
        elif term == 2:
            self.term_radio_buttons[0]['winter']['state'] = tk.DISABLED
        elif term == 3:
            self.term_radio_buttons[0]['summer']['state'] = tk.DISABLED
        self.deselect_term()

    def deselect_term(self):
        if self.term_radio_buttons[0]['fall']['state'] == tk.DISABLED:
            self.term_radio_buttons[0]['fall'].deselect()
            fall = False
        else:
            self.term_radio_buttons[0]['fall'].select()
            fall = True

        if self.term_radio_buttons[0]['winter']['state'] == tk.DISABLED:
            self.term_radio_buttons[0]['winter'].deselect()
            winter = False
        else:
            self.term_radio_buttons[0]['winter'].select()
            winter = True

        if self.term_radio_buttons[0]['summer']['state'] == tk.DISABLED:
            self.term_radio_buttons[0]['summer'].deselect()
            summer = False
        else:
            self.term_radio_buttons[0]['summer'].select()
            summer = True

        if not fall and not winter and not summer:
            self.term_var.set(0)
            self.ready_to_start()
            self.prompt_to_delete()

    def prompt_to_delete(self):
        pass

    def validate_term(self):
        if self.term_var:
            self.term_status.set('Done')
            self.term_radio_buttons[1]['fg'] = 'green'
        else:
            self.term_status.set('Select a Term')
            self.term_radio_buttons[1]['fg'] = 'red'
        self.ready_to_start()

    def create_export_label_frame(self):
        label_frame = tk.LabelFrame(self, text='Export To')
        gcal_radio = tk.Radiobutton(label_frame, text='Google Calendar',
                                    variable=self.export_var, value=1,
                                    command=self.check_export_option)
        csv_radio = tk.Radiobutton(label_frame, text='CSV File (.csv)',
                                   variable=self.export_var, value=2,
                                   command=self.check_export_option)
        ical_radio = tk.Radiobutton(label_frame, text='iCAL File (.ics)',
                                    variable=self.export_var, value=3,
                                    command=self.check_export_option)
        ical_radio['state'] = tk.DISABLED
        gcal_radio.grid(sticky=tk.W, row=0)
        gcal_radio.select()
        csv_radio.grid(sticky=tk.W, row=1)
        ical_radio.grid(sticky=tk.W, row=2)
        self.file_labelframe = self.create_file_labelframe(label_frame)
        self.deactivate_file_labelframe()
        label_frame.grid(columnspan=4, rowspan=6, row=4, sticky=tk.N)
        return label_frame

    def create_file_labelframe(self, parent=None):
        file_labelframe = tk.LabelFrame(parent, text='Save To')
        file_entry = tk.Entry(file_labelframe,
                              justify=tk.RIGHT,
                              textvariable=self.filepath)

        img = tk.PhotoImage(file=resource_path('img/folder.gif'))

        open_button = tk.Button(file_labelframe, image=img,
                                command=self.saveasfilename)
        open_button.image = img
        open_button.grid(row=0, column=1)
        file_entry.grid(row=0, column=0)

        file_labelframe.grid(columnspan=2, rowspan=2, row=1, column=3)
        return file_labelframe

    def activate_file_labelframe(self):
        for child in self.file_labelframe.children.values():
            child['state'] = tk.NORMAL

    def deactivate_file_labelframe(self):
        for child in self.file_labelframe.children.values():
            child['state'] = tk.DISABLED

    def check_export_option(self):
        if self.export_var.get() == 1:
            self.deactivate_file_labelframe()
        else:
            self.activate_file_labelframe()
            if self.export_var.get() == 2:
                self.file_opt = options = {}
                options['defaultextension'] = '.csv'
                options['initialfile'] = 'mycal.csv'
                options['title'] = 'Save As'
            else:
                self.file_opt = options = {}
                options['defaultextension'] = '.ics'
                options['initialfile'] = 'mycal.ics'
                options['title'] = 'Save As'

    def saveasfilename(self):
        self.filepath.set(asksaveasfilename(**self.file_opt))

    def create_optional_labelframe(self):
        opt_labelframe = tk.LabelFrame(self, text='Optional Settings')
        class_color_checkbox = tk.Checkbutton(opt_labelframe,
                                              text='Match event colors for '
                                                   'all classes in a course',
                                              variable=self.color_var)
        class_color_checkbox.select()
        roomnumber_checkbox = tk.Checkbutton(opt_labelframe,
                                             text='Place room number in '
                                                  'title',
                                             variable=self.room_var)
        location_checkbox = tk.Checkbutton(opt_labelframe,
                                           text='Set location to be '
                                                'compatible '
                                                'with google maps',
                                           variable=self.location_var)
        visibility_checkbox = tk.Checkbutton(opt_labelframe,
                                             text='Make events private',
                                             variable=self.privacy_var)
        status_checkbox = tk.Checkbutton(opt_labelframe,
                                         text='Show status as available',
                                         variable=self.availability_var)

        location_checkbox['state'] = tk.DISABLED
        status_checkbox['state'] = tk.DISABLED

        self.reminders_labelframe = self.create_reminders_labelframe(
            opt_labelframe)
        class_color_checkbox.grid(sticky=tk.W)
        roomnumber_checkbox.grid(sticky=tk.W)
        location_checkbox.grid(sticky=tk.W)
        visibility_checkbox.grid(sticky=tk.W)
        status_checkbox.grid(sticky=tk.W)
        self.reminders_labelframe.grid(rowspan=3, columnspan=3, sticky=tk.W)
        opt_labelframe.grid(rowspan=7, row=3, column=4, sticky=tk.N)
        return opt_labelframe

    def create_reminders_labelframe(self, parent=None):
        reminders_labelframe = tk.LabelFrame(parent,
                                             text='Reminders')
        reminders_checkbox = tk.Checkbutton(reminders_labelframe,
                                            text='Enable Reminders',
                                            variable=self.reminders_var,
                                            command=self.are_reminders_wanted)
        reminders_email_radio = tk.Radiobutton(reminders_labelframe,
                                               text='Email',
                                               value=1,
                                               variable=self.reminders_type,
                                               state=tk.DISABLED)
        reminders_popup_radio = tk.Radiobutton(reminders_labelframe,
                                               text='Pop-up',
                                               value=2,
                                               variable=self.reminders_type,
                                               state=tk.DISABLED)
        reminders_time_spin = tk.Spinbox(reminders_labelframe,
                                         from_=1, to=60,
                                         width=5,
                                         textvariable=self.reminders_time,
                                         state=tk.DISABLED)
        reminders_time_label = tk.Label(reminders_labelframe,
                                        text='Min', state=tk.DISABLED)
        reminders_popup_radio.select()
        reminders_checkbox.grid(sticky=tk.W)
        reminders_email_radio.grid(row=1, column=0, sticky=tk.E)
        reminders_popup_radio.grid(row=1, column=1, sticky=tk.W)
        reminders_time_spin.grid(row=1, column=2, sticky=tk.E)
        reminders_time_label.grid(row=1, column=3, sticky=tk.E)

        return reminders_labelframe

    def are_reminders_wanted(self):
        if self.reminders_var.get():
            status = tk.NORMAL
        else:
            status = tk.DISABLED

        for child in self.reminders_labelframe.children.values():
            if not isinstance(child, tk.Checkbutton):
                child['state'] = status

    def create_start_button(self):
        start_button = tk.Button(self, width='16', height=2, text='Start',
                                 command=self.validate_return,
                                 activebackground='green',
                                 activeforeground='white')

        start_button.grid(columnspan=2, row=9, column=0, sticky=tk.S + tk.W)
        start_button['state'] = tk.DISABLED
        return start_button

    def ready_to_start(self):
        if self.username_status.get() == 'Done' and \
                        self.password_status.get() == 'Done' and \
                self.term_var.get():
            self.start_button['state'] = tk.NORMAL
            self.start_button.flash()
            self.start_button.flash()
        else:
            self.start_button['state'] = tk.DISABLED

    def validate_return(self):
        ret = self.start_fnc(self.get_username(),
            self.get_password(),
            self.get_save_credentials(),
            self.get_term(),
            self.get_export_var(),
            self.get_color_bool(),
            self.get_room_bool(),
            self.get_location_bool(),
            self.get_privacy_bool(),
            self.get_availability_bool(),
            self.get_reminders_bool(),
            self.get_reminders_type(),
            self.get_reminders_time())
        if not ret:
            self.username.set('')
            self.username_status.set('Invalid Username. Please try again.')
            self.username_field[1]['fg'] = 'red'
            self.password.set('')
            self.password_status.set('Invalid Password. Please try again.')
            self.password_field[1]['fg'] = 'red'

        else:
            self.disable_term(self.term_var.get())

    def create_quit_button(self):
        quit_button = tk.Button(self, width='16', height=2, text='Cancel',
                                command=self.quit)
        quit_button.grid(columnspan=2, row=9, column=2, sticky=tk.S + tk.W)
        return quit_button

    def create_options_button(self):
        img = tk.PhotoImage(file=resource_path('img/options.gif'))
        options_button = tk.Button(self, height=38, width=47, image=img,
                                   command=self.create_options_window)
        options_button.image = img
        options_button.grid(row=9, column=3, sticky=tk.S + tk.E)
        return options_button

    def create_options_window(self):
        window = tk.Toplevel(self)
        center(window)
        window.wm_title('Options')

        # self.clearrecent_button = tk.Button(window,
        #                                     text='Delete Recent uCal Events',
        #                                     command=self.clear_current_events()
        #                                     )

        self.clearall_button = tk.Button(window, text='Delete All uCal Events',
                                         command=self.clear_all_events)

        self.cleargoogle_button = tk.Button(window, text='Deactivate google '
                                                         'account',
                                            command=self.deactivate_google)

        self.disable_clear_all()
        self.disable_google_button()
        self.clearall_button.pack()
        self.cleargoogle_button.pack()

    def disable_clear_all(self):
        if not os.listdir(resource_path('events')):
            self.clearall_button['state'] = tk.DISABLED
        else:
            self.clearall_button['state'] = tk.NORMAL

    # def clear_current_events(self):
    #     self.clearreccent_fnc()

    def clear_all_events(self):
        self.clear_fnc()
        self.term_radio_buttons[0]['fall']['state'] = tk.NORMAL
        self.term_radio_buttons[0]['winter']['state'] = tk.NORMAL
        self.deselect_term()

    def disable_google_button(self):
        if os.path.exists(resource_path('.credentials/ucal.json')):
            self.cleargoogle_button['state'] = tk.NORMAL
        else:
            self.cleargoogle_button['state'] = tk.DISABLED

    def deactivate_google(self):
        if os.path.exists(resource_path('.credentials/ucal.json')):
            os.remove(resource_path('.credentials/ucal.json'))
        self.disable_google_button()


if __name__ == '__main__':
    def fake():
        print 'fake'

    app = GUI(fake, fake)
    app.master.title('uCal - Import your UOIT schedule to google calendar')
    app.mainloop()