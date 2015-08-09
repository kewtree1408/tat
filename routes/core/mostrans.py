# -*- coding: utf8 -*-

import html5lib
import requests
import logging
import urllib

from urlparse import urljoin, urlparse, parse_qsl
from datetime import time
from django.db import transaction

from .models import TatType, Waypoint, WaypointTime, Route, Direction, Stop
from .utils import humanized_days_to_flags

mosgortrans_url = 'http://www.mosgortrans.org/pass3/simplified.php'
session = requests.session()
logger = logging.getLogger(__name__)


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
    for t, tu in get_parsed_items(url):
        tat_type, created = TatType.objects.get_or_create(title=t)
        tat_type = tat_type or created
        for number, number_url in get_parsed_items(tu):  # numbers
            if number == '0':
                continue
            if only_numbers and number not in map(lambda x: x.decode('utf-8'), only_numbers):
                continue
            print(u'Обновляется {type} {number}'.format(type=tat_type, number=number))
            route, created = Route.objects.get_or_create(tat_number=number, tat_type=tat_type)
            route = route or created
            # применять изменения нужно разом для всего маршрута
            with transaction.atomic():
                Direction.objects.filter(route=route).delete()  # удалим старое перед добавлением

                for days, days_url in get_parsed_items(number_url):  # days
                    for direction, direction_url in get_parsed_items(woodleg_for_url(days_url)):  # routes
                        direction, created = Direction.objects.get_or_create(title=direction, route=route)
                        direction = direction or created
                        # routes
                        for i, (stop, stop_url) in enumerate(get_parsed_items(woodleg_for_url(direction_url))):
                            if stop.lower().strip() == u'все остановки маршрута':
                                continue
                            stop, created = Stop.objects.get_or_create(title=stop)
                            stop = stop or created
                            waypoint, created = Waypoint.objects.get_or_create(stop=stop, direction=direction, order=i)
                            waypoint = waypoint or created
                            for time in get_parsed_times(woodleg_for_url(stop_url)):
                                WaypointTime.objects.create(
                                    time=time, waypoint=waypoint, weekdays=humanized_days_to_flags(days)
                                )
