# -*- coding: utf8 -*-

import html5lib
import requests
import logging
import urllib
import pymongo

from urlparse import urljoin
from datetime import time


mosgortrans_url = 'http://www.mosgortrans.org/pass3/simplified.php'
session = requests.session()
logger = logging.getLogger(__name__)
db = pymongo.Connection().tat


TAT_TYPES = {
    u'Автобус': 'avto',
    u'Троллейбус': 'trol',
    u'Трамвай': 'tram',
}


WEEKDAYS = {
    u'единый': [0, 1, 2, 3, 4, 5, 6],
    u'будни': [0, 1, 2, 3, 4],
    u'выходные': [5, 6],
    u'понедельник': [0],
    u'вторник': [1],
    u'среда': [2],
    u'четверг': [3],
    u'пятница': [4],
    u'суббота': [5],
    u'воскресение': [6],
}


def humanized_days_to_array(humanized_days):
    if not humanized_days:
        return []
    humanized_days = humanized_days.lower().strip()
    if ',' in humanized_days:
        result = []
        for day in humanized_days.split(','):
            result += humanized_days_to_array(day)
        return result
    for ru_name in WEEKDAYS:
        if ru_name == humanized_days:
            return WEEKDAYS[ru_name]


def humanize_days(flags):
    for name, ru_name, value in WEEKDAYS:
        if value == int(flags):
            return ru_name


def get_parsed_items(url):
    html = html5lib.parse(
        session.get(url).content.decode('cp1251'),
        treebuilder="lxml",
        namespaceHTMLElements=False,
    ).getroot()
    for a in html.xpath('//body/ul/li/a'):
        item_title = a.text
        item_url = urljoin(url, a.attrib['href'])
        logger.debug('Found item name=%s url=%s', item_title, item_url)
        yield item_title, item_url


def get_parsed_times(url):
    html = html5lib.parse(
        session.get(url).text,
        treebuilder="lxml",
        namespaceHTMLElements=False,
    ).getroot()
    for item in html.xpath('//table/tbody/tr/td/span[@class="hour" or @class="minutes"]'):
        if item.attrib['class'] == 'hour' and item.text and item.text.isdigit():
            hour = int(item.text)
        elif item.attrib['class'] == 'minutes' and item.text and item.text.isdigit():
            minutes = int(item.text)
            logger.debug('Found time %s:%s', hour, minutes)
            yield time(hour, int(minutes))


def woodleg_for_url(url):
    try:
        res_url = url.encode('cp1251').decode('utf-8')
    except:
        res_url = url
    for char in u'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮ':
        if char in res_url:
            res_url = res_url.replace(char, urllib.quote(char.encode('cp1251')))
    return res_url


def fetch(url=mosgortrans_url, only_numbers=None):
    doc = {}
    for tat_type, tu in get_parsed_items(url):
        doc['type'] = TAT_TYPES[tat_type]
        for number, number_url in get_parsed_items(tu):  # numbers
            if number == '0':
                continue
            if only_numbers and number not in map(lambda x: x.decode('utf-8'), only_numbers):
                continue
            print(u'Обновляется {type} {number}'.format(type=tat_type, number=number).encode('utf-8'))
            doc['number'] = number
            for days, days_url in get_parsed_items(number_url):  # days
                doc['days'] = humanized_days_to_array(days)
                for direction, direction_url in get_parsed_items(woodleg_for_url(days_url)):  # routes
                    doc['direction'] = direction
                    # routes
                    for i, (stop, stop_url) in enumerate(get_parsed_items(woodleg_for_url(direction_url))):
                        if stop.lower().strip() == u'все остановки маршрута':
                            continue
                        doc['stop'] = stop
                        doc['times'] = [(t.hour, t.minute) for t in get_parsed_times(woodleg_for_url(stop_url))]
                        db.waypoints.insert(doc.copy())


if __name__ == '__main__':
    fetch()
