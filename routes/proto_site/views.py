# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from forms import RouteSearch, StopSearch
from core.models import Route, Stop

from django.views.decorators.cache import cache_page

@cache_page(60 * 15)
def index(request):
    max_order_count = 20
    max_times_count = 10
    context = {
        'range_counters': range(0, max_order_count),
        'range_times': range(0, max_times_count),
    }
    route_form = RouteSearch(number='')
    stop_form = StopSearch(name='')
    context['route_form'] = route_form
    context['stop_form'] = stop_form
    return render(request, 'proto_site/index.html', context)


@cache_page(60 * 15)
def times(request, idx):
    days = ('Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота')
    idxs = (i for i in range(0,7))
    weekdays = zip(idxs, days)
    count_times = 24*60;
    # count_hours = 20

    context = {
                'weekdays': weekdays,
                'id':idx,
                'range_times': range(0, count_times),
                # 'range_hours': range(0, count_hours),
            }
    return render(request, 'proto_site/times.html', context)


@cache_page(60 * 15)
def route_suggest(request):
    number = request.GET.get('query')
    if not number:
        return HttpResponse(json.dumps({'options': []}), content_type='application/json')
    rl = [r.route_name for r in Route.objects.filter(tat_number__contains=number)[:10]]
    return HttpResponse(json.dumps({'options': sorted(rl)}), content_type='application/json')


@cache_page(60 * 15)
def stop_suggest(request):
    name = request.GET.get('query')
    if not name:
        return HttpResponse(json.dumps({'options': []}), content_type='application/json')
    sl = [s.title for s in Stop.objects.filter(title__icontains=name)[:10]]
    return HttpResponse(json.dumps({'options': sorted(sl)}), content_type='application/json')


def test_backbone(request):
    context = {}
    return render(request, 'proto_site/index2.html', context)