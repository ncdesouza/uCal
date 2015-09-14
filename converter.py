from datastructures import *


class Converter:
    def __init__(self, color_bool, room_bool, location_bool, private_bool,
                 status_bool, reminders_bool, reminders_type, reminders_time):
        self.color_bool = color_bool
        self.room_bool = room_bool
        self.location_bool = location_bool
        self.private_bool = private_bool
        self.status_bool = status_bool
        self.reminders_bool = reminders_bool
        self.reminders_type = reminders_type
        self.reminders_time = reminders_time

        self.color_ids = iter(['6', '4', '8', '2', '5', '1', '7', '3', '9',
                              '10'])
        self.cur_color = None

    def convert_uschedule_to_gevent(self, schedule):
        for cls in schedule:
            assert isinstance(cls, Class)

        events = []
        prev_class = None

        for cls in schedule:
            # print cls

            # create some
            tmp = []
            cur_class = cls.title[:cls.title.rfind('-')].rstrip()
            if cur_class != prev_class:
                self.cur_color = self.color_ids.next()
                prev_class = cur_class

            for meeting in cls.meeting_times:
                # Build
                if meeting.time == 'TBA' or meeting.where == 'TBA':
                    continue
                summary = self.convert_title(cls.title, meeting.where)
                location = self.convert_location(meeting.where)
                description = self.convert_description(cls.instructor,
                                                       cls.crn, cls.title,
                                                       meeting.schedule_type)

                dates = self.convert_dates(meeting.date_range, meeting.time,
                                           meeting.day)
                if not dates['until']:
                    tmp.append(dates)
                    if cls.meeting_times.index(meeting) == \
                                                len(cls.meeting_times) - 1:

                        events.append(self.build_event(summary, location,
                                                       description,
                                                       tmp[0]['startDate'],
                                                       tmp[0]['endDate'],
                                                       reccurringDates=
                                                       [d['startDate'] for d
                                                        in tmp[1:]],
                                                       colorId=self.cur_color))
                else:
                    events.append(self.build_event(summary, location,
                                                   description,
                                                   dates['startDate'],
                                                   dates['endDate'],
                                                   reccurring_endDate=dates[
                                                       'until'],
                                                   colorId=self.cur_color))
        return events

    def convert_dates(self, date_str, time_str, day_char):
        date = {}
        # parse start date and end date
        start_date_str = date_str[:date_str.find('-')].rstrip()
        end_date_str = date_str[date_str.find('-')+1:].lstrip()

        # if the dates are not the same it means a date range is given
        if start_date_str != end_date_str:
            # create an until date, equal to the end of day on end date
            until_date_str = end_date_str
            until_date_str += ' 11:00 PM'
            date['until'] = datetime.datetime.strptime(until_date_str,
                                                       '%b %d, %Y %I:%M %p')
            end_date_str = start_date_str
        else:  # otherwise a single date was given
            date['until'] = None

        # parse the start time and end time
        start_date_str += ' ' + time_str[:time_str.find('-')].rstrip().upper()
        end_date_str += ' ' + time_str[time_str.find('-')+1:].lstrip().upper()

        toronto = pytz.timezone('America/Toronto')

        # build the start date and end date
        date['startDate'] = datetime.datetime.strptime(start_date_str,
                                                       '%b %d, %Y %I:%M %p')

        date['endDate'] = datetime.datetime.strptime(end_date_str,
                                                     '%b %d, %Y %I:%M %p')

        if date['until']:
            date['startDate'] = self.correct_day(date['startDate'], day_char)
            date['endDate'] = self.correct_day(date['endDate'], day_char)

        return date

    def correct_day(self, date, weekday):
        if weekday == 'M':
            day = 0
        elif weekday == 'T':
            day = 1
        elif weekday == 'W':
            day = 2
        elif weekday == 'R':
            day = 3
        else:
            day = 4
        days_ahead = day - date.weekday()
        if days_ahead < 0:
            days_ahead += 7
        new_date = date + datetime.timedelta(days_ahead)
        # print (days_ahead,  weekday, 'before: ' + date.strftime('%a %B %d'),
        #        'after: ' + new_date.strftime('%a %B %d'))
        return new_date

    def convert_title(self, title, where):
        summary = title[:title.rfind('-')].rstrip()
        if self.room_bool:
            summary = self.convert_location(where) + ' - ' + summary
        return summary

    def convert_location(self, where):
        location = where[where.rfind(' '):].lstrip()
        return location

    def convert_description(self, instructor, crn, title, schedule_type):
        description = 'Schedule Type: ' + schedule_type + '\n'
        description += 'CRN: ' + crn + '\n'
        description += 'Section: ' + title[title.rfind('-')+1:].lstrip() + '\n'
        description += 'Instructor: ' + instructor

        return description

    def build_event(self, summary, location, description, start_dateTime,
                    end_dateTime, colorId=None,
                    reccurring_endDate=None, reccurringDates=None):
        if self.private_bool:
            visibility = 'private'
        else:
            visibility = 'default'

        if self.reminders_bool and self.color_bool:
            event = ColoredReminderRecurringEvent(summary, location,
                                                  description, start_dateTime,
                                                  end_dateTime, visibility,
                                                  colorId,
                                                  self.reminders_type,
                                                  self.reminders_time,
                                                  reccurring_endDate,
                                                  reccurringDates)
        elif self.reminders_bool:
            event = ReminderRecurringEvent(summary, location, description,
                                           start_dateTime, end_dateTime,
                                           visibility,
                                           self.reminders_type,
                                           self.reminders_time,
                                           reccurring_endDate,
                                           reccurringDates)
        elif self.color_bool:
            event = ColoredRecurringEvent(summary, location, description,
                                           start_dateTime, end_dateTime,
                                           visibility, colorId,
                                           reccurring_endDate,
                                           reccurringDates)
        else:
            event = RecurringEvent(summary, location, description,
                                   start_dateTime, end_dateTime, visibility,
                                   reccurring_endDate, reccurringDates)
        return event

if __name__ == '__main__':
    converter = Converter(False, True, False, False,False,False,False,False)
