# -*- coding: utf-8 -*-

import simplejson
from django import forms
from django.forms import widgets
from core.models import Route, Stop


class RouteSearch(forms.Form):
    route = forms.CharField(
        label=u'Поиск по маршруту',
        required=True)

    def __init__(self, number, *args, **kwargs):
        super(RouteSearch, self).__init__(*args, **kwargs)

        self.widget = forms.TextInput(attrs={
            'class': 'text ajax-typeahead',
            'data-link': '/prototype/route_suggest'
        })

        self.fields['route'] = forms.CharField(
            label=u'Поиск по маршруту',
            required=True,
            widget=self.widget,
        )


class StopSearch(forms.Form):
    stop = forms.CharField(
        label=u'Поиск по названию остановки',
        required=True)

    def __init__(self, name, *args, **kwargs):
        super(StopSearch, self).__init__(*args, **kwargs)

        self.widget = forms.TextInput(attrs={
            'class': 'text ajax-typeahead',
            'data-link': '/prototype/stop_suggest'
        })

        self.fields['stop'] = forms.CharField(
            label=u'Поиск по названию остановки',
            required=True,
            widget=self.widget,
        )
