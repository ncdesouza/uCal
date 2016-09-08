import datetime
import pytz


class Class:
    def __init__(self, title, associated_term, crn, status, instructor,
                 credit):
        self.title = title
        self.associated_term = associated_term
        self.crn = crn
        self.status = status
        self.instructor = instructor
        self.credit = credit
        self.meeting_times = []

    def add_meeting_time(self, meeting_time):
        assert isinstance(meeting_time, MeetingTime)
        self.meeting_times.append(meeting_time)

    def __repr__(self):
        time_str = '{0:^4} {1:^6} {2:^20} {3:^3} {4:^30} {5:^30} {6:^15} ' \
                   '{7:^25}\n'.format('Week', 'Type', 'Time', 'Day', 'Where',
                                      'Date Range', 'Schedule Type', 'Instructor')
        for meeting_time in self.meeting_times:
            time_str += str(meeting_time)

        return '   Course Title: ' + str(self.title) + '\n' \
               'Associated Term: ' + str(self.associated_term) + '\n' \
               '            CRN: ' + str(self.crn) + '\n' \
               '         Status: ' + str(self.status) + '\n' \
               '     Instructor: ' + str(self.instructor) + '\n' \
               '         Credit: ' + str(self.credit) + '\n' \
               'Scheduled Meeting Times \n' \
               + time_str


class MeetingTime:
    def __init__(self, week, type_, time, day, where, date_range,
                 schedule_type, instructors):
        self.week = week
        self.type = type_
        self.time = time
        self.day = day
        self.where = where
        self.date_range = date_range
        self.schedule_type = schedule_type
        self.instructors = instructors

    def __repr__(self):
        return '{0:^4} {1:^6} {2:^20} {3:^3} {4:^30} {5:^30} {6:^15} {7:^25}' \
               '\n'.format(self.week, self.type, self.time, self.day,
                           self.where, self.date_range, self.schedule_type,
                           self.instructors)


class Event:
    def __init__(self, summary, location, description, start_dateTime,
                 end_dateTime, visibility):
        self.kind = 'calendar#event'
        self.summary = str(summary)
        self.location = str(location)
        self.description = str(description)
        self.start = {
            'dateTime': self.date_to_datetimezone_string(start_dateTime),
            'timeZone': 'America/Toronto'}
        self.end = {
            'dateTime': self.date_to_datetimezone_string(end_dateTime),
            'timeZone': 'America/Toronto'}
        self.visibility = visibility

    @staticmethod
    def date_to_datetimezone_string(date):
        assert isinstance(date, datetime.datetime)
        toronto = pytz.timezone('America/Toronto')
        tzdate = toronto.localize(date)
        return tzdate.strftime('%Y-%m-%dT%H:%M:%S%z')

    def __repr__(self):
        return str(self.__dict__)

    def get_dict(self):
        return self.__dict__


class RecurringEvent(Event):
    def __init__(self, summary, location, description, start_dateTime,
                 end_dateTime, visibility, recurring_endDate=None,
                 recurring_dates=None):
        if not recurring_dates:
            recurring_dates = []
        Event.__init__(self, summary, location, description, start_dateTime,
                       end_dateTime, visibility)
        self.recurrence = self.build_recurring_rules(recurring_endDate,
                                                     recurring_dates,
                                                     start_dateTime)

    def build_recurring_rules(self, recurring_endDate, recurring_dates,
                              start_date):
        assert isinstance(start_date, datetime.datetime)
        if recurring_endDate:
            rec_rules = 'RRULE:'
            rec_rules += self.build_recurring_frequency() + ';'
            rec_rules += self.build_recurring_end_date(recurring_endDate)
            rec_excep = self.build_recurring_exception(start_date)

            # if start_date.weekday() == 0 and start_date.year == 2015 and 9 <= start_date.month <= 12:
            #     weird_date = datetime.datetime(2015, 12, 3, start_date.hour,
            #                                    start_date.minute)
            #     rec_dates = self.build_recurring_dates([weird_date])
            #     return [rec_rules, rec_dates, rec_excep]
            # if start_date.weekday() == 4 and start_date.year == 2016 and 1 <= start_date.month <= 4:
            #     weird_date = datetime.datetime(2016, 4, 11, start_date.hour, start_date.minute)
            #     rec_dates = self.build_recurring_dates([weird_date])
            #     return [rec_rules, rec_dates, rec_excep]

            return [rec_rules, rec_excep]
        elif recurring_dates:
            rec_date = self.build_recurring_dates(recurring_dates)
            rec_excep = self.build_recurring_exception(start_date)
            return [rec_date, rec_excep]

    def build_recurring_frequency(self):
        rec_freq = 'FREQ=WEEKLY'
        return rec_freq

    def build_recurring_end_date(self, date):
        rec_end = 'UNTIL='
        rec_end += self.date_to_datetime_string(date) + 'Z'
        return rec_end

    def build_recurring_dates(self, dates):
        assert isinstance(dates, list)
        rec_dates = 'RDATE;TZID=America/Toronto;VALUE=DATE:'
        for date in dates[:-1]:
            rec_dates += self.date_to_datetime_string(date) + ','
        rec_dates += self.date_to_datetime_string(dates[-1])
        return rec_dates

    def build_recurring_exception(self, start):
        assert isinstance(start, datetime.datetime)
        excep1 = datetime.datetime(2016, 10, 10, start.hour, start.minute)
        excep3 = datetime.datetime(2017, 2, 20, start.hour, start.minute)
        excep4 = datetime.datetime(2017, 2, 21, start.hour, start.minute)
        excep5 = datetime.datetime(2017, 2, 22, start.hour, start.minute)
        excep6 = datetime.datetime(2017, 2, 23, start.hour, start.minute)
        excep7 = datetime.datetime(2017, 2, 24, start.hour, start.minute)
        excep8 = datetime.datetime(2017, 2, 25, start.hour, start.minute)
        excep9 = datetime.datetime(2017, 2, 26, start.hour, start.minute)
        excep10 = datetime.datetime(2017, 4, 14, start.hour, start.minute)

        excep_dates = [excep1, excep3, excep4, excep5, excep6,
                       excep7, excep8, excep9, excep10]
        except_str = 'EXDATE;TZID=America/Toronto:'
        for date in excep_dates[:-1]:
            except_str += self.date_to_datetime_string(date) + ','
        except_str += self.date_to_datetime_string(excep_dates[-1])
        return except_str

    @staticmethod
    def date_to_datetime_string(date):
        assert isinstance(date, datetime.datetime)
        return date.strftime('%Y%m%dT%H%M%S')

    @staticmethod
    def date_to_date_string(date):
        assert isinstance(date, datetime.datetime)
        return date.strftime('%Y%m%d')

    @staticmethod
    def to_datetimezone_string(date):
        assert isinstance(date, datetime.datetime)
        toronto = pytz.timezone('America/Toronto')
        tzdate = toronto.localize(date)
        return tzdate.strftime('%Y%m%dT%H%M%S%z')


class ReminderRecurringEvent(RecurringEvent):
    def __init__(self, summary, location, description, start_dateTime,
                 end_dateTime, visibility, reminderMethod, reminderTime,
                 recurring_endDate=None, recurring_dates=None):
        RecurringEvent.__init__(self, summary, location, description,
                                start_dateTime, end_dateTime, visibility,
                                recurring_endDate, recurring_dates)
        self.reminders = {'useDefault': False,
                          'overrides': [
                              {'method': reminderMethod,
                               'minutes': reminderTime}
                          ]}


class ColoredRecurringEvent(RecurringEvent):
    def __init__(self, summary, location, description, start_dateTime,
                 end_dateTime, visibility, colorId, recurring_endDate=None,
                 recurring_dates=None):
        RecurringEvent.__init__(self, summary, location, description,
                                start_dateTime, end_dateTime, visibility,
                                recurring_endDate, recurring_dates)
        self.colorId = colorId


class ColoredReminderRecurringEvent(ReminderRecurringEvent):
    def __init__(self, summary, location, description, start_dateTime,
                 end_dateTime, visibility, colorId, reminderMethod,
                 reminderTime, recurring_endDate=None, recurring_dates=None):
        ReminderRecurringEvent.__init__(self, summary, location, description,
                                        start_dateTime, end_dateTime,
                                        visibility, reminderMethod,
                                        reminderTime, recurring_endDate,
                                        recurring_dates)
        self.colorId = colorId