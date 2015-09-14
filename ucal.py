import csv
import os
import sys
from gui import GUI
from gcal import GCal
from datastructures import Class, MeetingTime
from converter import Converter

import json
from splinter import Browser


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class UCal:
    def __init__(self):
        self.username = None
        self.password = None
        self.term = None
        self.browser = None
        self.commands = (self.login, self.go_to_schedule,
                         self.choose_term, self.get_schedule)

        self.recent_events = None

    def start(self, username, password, save_credentials_bool, term, export,
              color_bool, room_bool, location_bool, privacy_bool,
              availability_bool, reminders_bool, reminders_type,
              reminders_time):
        self.set_username(username)
        self.set_password(password)

        if save_credentials_bool:
            with open(resource_path('save.json'), 'w') as f:
                json.dump({'username': self.username,
                           'password': self.password},
                          f)

        # if export == 'google calendar':
        exporter = GCal()

        self.set_term(term)
        data = []
        with Browser() as self.browser:
            for cmd in self.commands:
                data = cmd()
                if not data:
                    return False

        converter = Converter(color_bool, room_bool, location_bool,
                              privacy_bool, availability_bool,
                              reminders_bool, reminders_type, reminders_time)

        events = converter.convert_uschedule_to_gevent(data)

        added_events = []

        for event in events:
            print event
            added_event = exporter.add_event(event.get_dict())
            added_events.append(added_event)

        self.save_events(added_events)

        return True

    def save_events(self, events):
        directory = 'events'
        filename = 'events' + str(self.term)
        i = 0
        if not os.path.exists(resource_path(directory)):
            os.mkdir(resource_path(directory))
        else:
            files = os.listdir(resource_path(directory))
            for f in files:
                append = '(' + str(i) + ')'
                if f == filename + '.json' or f == filename + append + '.json':
                    i += 1

        if i > 0:
            filename += '(' + str(i) + ')'
        filename += '.json'

        with open(resource_path(directory + '/' + filename), 'w') as f:
            json.dump(events, f)

    def clear_recent(self):
        pass

    def clear_term(self, term):
        pass

    def clear_all(self):
        gcal = GCal()
        event_files = os.listdir(resource_path('events'))
        for ef in event_files:
            with open(resource_path('events/' + ef), 'r') as f:
                events = json.load(f)
                for event in events:
                    gcal.del_event(event['id'])

            os.remove(resource_path('events/' + ef))





    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_term(self, term):
        self.term = term

    def login(self):
        self.browser.visit('http://www.uoit.ca/mycampus/')
        self.browser.fill('user', self.username)
        self.browser.fill('pass', self.password)

        button = self.browser.find_by_value('Login')
        button.click()

        if self.browser.title == 'Error: Failed Login':
            return False
        return True

    def go_to_schedule(self):
        self.browser.click_link_by_href(
            '/cp/render.UserLayoutRootNode.uP?uP_tparam=utf'
            '&utf=/cp/school/sctmain')

        with self.browser.get_iframe('content') as iframe:
            try:
                iframe.click_link_by_partial_text('Student')
                iframe.click_link_by_partial_text('Registration')
                iframe.click_link_by_partial_text('Student Detail Schedule')
            except Exception:
                return False
            return True

    def choose_term(self):
        with self.browser.get_iframe('content') as iframe:
            try:
                iframe.select('term_in', self.term)
                iframe.find_by_value('Submit').click()
            except Exception:
                return False
            return True

    def get_schedule(self):
        with self.browser.get_iframe('content') as iframe:

            body_div = iframe.find_by_css('DIV.pagebodydiv')
            tables = body_div.first.find_by_tag('table')

            for table in tables:
                if not table.has_class('bordertable'):
                    tables.remove(table)

            classes = []
            i = 0
            while i < len(tables):
                classes.append({'info': tables[i], 'time': tables[i + 1]})
                i += 2

            class_data = []

            for c in classes:
                title = c['info'].find_by_tag('caption')
                rows = c['info'].find_by_tag('tr')
                text = (title.text, )
                for row in rows:
                    fields = row.find_by_tag('td')
                    for field in fields:
                        if field.has_class('dbdefault'):
                            text += (field.text,)

                cls = Class(*text)
                rows = c['time'].find_by_tag('tr')
                for row in rows:
                    text = ()
                    fields = row.find_by_tag('td')
                    for field in fields:
                        if field.has_class('dbdefault'):
                            text += (field.text,)
                    if len(text) == 8:
                        cls.add_meeting_time(MeetingTime(*text))

                class_data.append(cls)

            return class_data


def run():
    if os.path.isfile('save.json'):
        try:
            with open('save.json') as f:
                save = json.load(f)
        except ValueError:
            os.remove('save.json')
            save = dict(username=None, password=None)
    else:
        save = dict(username=None, password=None)
    ucal = UCal()
    gui = GUI(ucal.start, ucal.clear_all,
              save['username'], save['password'])
    gui.master.title('uCal - Import your UOIT schedule to google calendar')
    gui.mainloop()


if __name__ == '__main__':
    run()
    # ucal = UCal()
    # ucal.clear_all()
