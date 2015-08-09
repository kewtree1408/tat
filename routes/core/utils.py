# -*- coding: utf8 -*-

from .models import WaypointTime

WEEKDAYS = (
    ('all', u'единый', (
        WaypointTime.weekdays.monday
        | WaypointTime.weekdays.tuesday
        | WaypointTime.weekdays.wednesday
        | WaypointTime.weekdays.thursday
        | WaypointTime.weekdays.friday
        | WaypointTime.weekdays.saturday
        | WaypointTime.weekdays.sunday
    )),
    ('workdays', u'будни', (
        WaypointTime.weekdays.monday
        | WaypointTime.weekdays.tuesday
        | WaypointTime.weekdays.wednesday
        | WaypointTime.weekdays.thursday
        | WaypointTime.weekdays.friday
    )),
    ('weekend', u'выходные', WaypointTime.weekdays.saturday | WaypointTime.weekdays.sunday),
    ('monday', u'понедельник', WaypointTime.weekdays.monday),
    ('tuesday', u'вторник', WaypointTime.weekdays.tuesday),
    ('wednesday', u'среда', WaypointTime.weekdays.wednesday),
    ('thursday', u'четверг', WaypointTime.weekdays.thursday),
    ('friday', u'пятница', WaypointTime.weekdays.friday),
    ('saturday', u'суббота', WaypointTime.weekdays.saturday),
    ('sunday', u'воскресенье', WaypointTime.weekdays.sunday),
)


def humanized_days_to_flags(humanized_days):
    humanized_days = humanized_days.lower().strip()
    if ',' in humanized_days:
        result = 0
        for day in humanized_days.split(','):
            result |= humanized_days_to_flags(day)
        return result
    for name, ru_name, value in WEEKDAYS:
        if name == humanized_days or ru_name == humanized_days:
            return value


def humanize_days(flags):
    for name, ru_name, value in WEEKDAYS:
        if value == int(flags):
            return ru_name
