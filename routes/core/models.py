# -*- coding:  utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from bitfield import BitField


class TatType(models.Model):

    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = _(u'Тип транспорта')
        verbose_name_plural = _(u'Типы транспорта')

    def __unicode__(self):
        return self.title


class Stop(models.Model):

    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = _(u'Остановка')
        verbose_name_plural = _(u'Остановки')

    def __unicode__(self):
        return u'%s'%self.title


class Route(models.Model):

    tat_number = models.CharField(max_length=50)
    tat_type = models.ForeignKey(TatType)

    class Meta:
        verbose_name = _(u'Маршрут')
        verbose_name_plural = _(u'Маршруты')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.tat_number, self.tat_type)

    @property
    def route_name(self):
        return u'{0} {1}'.format(self.tat_number, self.tat_type)


class Direction(models.Model):

    title = models.CharField(max_length=100)
    route = models.ForeignKey(Route)

    class Meta:
        verbose_name = _(u'Направление')
        verbose_name_plural = _(u'Направления')

    def __unicode__(self):
        return u'{1}: {0}'.format(self.title, self.route)


class Waypoint(models.Model):

    stop = models.ForeignKey(Stop)
    direction = models.ForeignKey(Direction)
    order = models.SmallIntegerField()

    class Meta:
        verbose_name = _(u'Остановка на пути')
        verbose_name_plural = _(u'Остановки на пути')

    def __unicode__(self):
        return u'{0} <{2}>'.format(self.stop, self.direction, self.order)

    @property
    def tat_number(self):
        return self.direction.route.tat_number

    @property
    def tat_type(self):
        return self.direction.route.tat_type.title

    @property
    def route_title(self):
        return u'{0} {1}'.format(self.tat_number, self.tat_type)

    @property
    def stop_title(self):
        return self.stop.title

    @property
    def direction_title(self):
        return self.direction.title


class WaypointTime(models.Model):

    waypoint = models.ForeignKey(Waypoint)
    time = models.TimeField()
    weekdays = BitField(flags=(
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ))


    class Meta:
        verbose_name = _(u'Время остановки')
        verbose_name_plural = _(u'Времена остановок')

    def __unicode__(self):
        from .utils import humanize_days

        return u'{0} - {2} ({1})'.format(self.waypoint, self.time,  humanize_days(self.weekdays))

    @property
    def stop_title(self):
        return self.waypoint.stop.title

    @property
    def days(self):
        from .utils import humanize_days

        return humanize_days(self.weekdays)

    @property
    def route_title(self):
        return u'{0} {1}'.format(self.waypoint.tat_number, self.waypoint.tat_type)

    @property
    def direction_title(self):
        return self.waypoint.direction.title

    @property
    def order(self):
        return int(self.waypoint.order)
