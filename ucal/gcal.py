import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class GCal:
    def __init__(self):
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'ucal'
        self.flags = flags
        self.service = self.start_service()

    def authorize(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        return http

    def start_service(self):
        service = discovery.build('calendar', 'v3', http=self.authorize())
        return service

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_dir = resource_path('.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'ucal.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:

            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)

            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    def add_event(self, event):
        """Adds an Event to google Calendar.
            :param events
                A list of events of type Event.
        """
        assert isinstance(event, dict)
        new_event = self.service.events().insert(calendarId='primary',
                                                 body=event).execute()
        print 'Event created: %s' % (new_event.get('htmlLink'))
        return new_event

    def get_colors(self):
        colors = self.service.colors().get().execute()
        for id_, color in colors['event'].iteritems():
            print id_, color['background'], color['foreground']

    def del_event(self, eventId):
        self.service.events().delete(calendarId='primary',
                                     eventId=eventId).execute()

    def clear(self):
        self.service.calendars().clear(calendarId='primary').execute()



if __name__ == '__main__':
    gcal = GCal()
    gcal.clear()