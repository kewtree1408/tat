from django.http import Http404
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from core.utils import humanized_days_to_flags
from core.models import TatType, Stop, Route, Direction, Waypoint, WaypointTime

from serializers import StopSerializer, TimeSerializer, RouteSerializer, TimeWithDirectionSerializer, InputSerializer

import datetime


class StopDetail(APIView):

    def get_object(self, pk):
        try:
            return Stop.objects.get(pk=pk)
        except Stop.DoesNotExist:
            raise Http404

    def get_stops(self, **kw):
        number, tp = kw.get('number'), kw.get('type')
        return Waypoint.objects.filter(direction__route__tat_number=number, direction__route__tat_type__title=tp).order_by('direction__title')

    def get(self, request, **kw):
        stop = self.get_stops(**kw)
        serializer = StopSerializer(stop)
        return Response(serializer.data)


class TimeDetail(APIView):

    def get_times_with_directions(self, number, tp, stop, day):
        tp = TatType.objects.get(title=tp)
        stop = Stop.objects.get(title=stop)
        route = Route.objects.get(Q(tat_number=number), Q(tat_type__id=tp.id))
        d = Direction.objects.filter(route__id=route.id)
        waypoint = Waypoint.objects.filter(stop__id=stop.id, direction__in=d)
        return WaypointTime.objects.filter(waypoint__in=waypoint, weekdays=humanized_days_to_flags(day)).order_by('waypoint__direction__title')


    def get_times(self, number, tp, stop, day, time, n=10):
        tp = TatType.objects.get(title=tp)
        stop = Stop.objects.get(title=stop)
        route = Route.objects.get(Q(tat_number=number), Q(tat_type__id=tp.id))
        d = Direction.objects.filter(route__id=route.id)
        waypoint = Waypoint.objects.filter(stop__id=stop.id, direction__in=d)
        return WaypointTime.objects.filter(time__gt=time, waypoint__in=waypoint, weekdays=humanized_days_to_flags(day)).all()[:n]

    def get(self, request, **kw):
        number, tp, stop, day, time = (kw.get(key) for key in ['number', 'type', 'stop', 'day', 'time'])
        if time:
            waypointtime = self.get_times(number, tp, stop, day, time)
            serializer = TimeSerializer(waypointtime)
        else:
            waypointtime = self.get_times_with_directions(number, tp, stop, day)
            serializer = TimeWithDirectionSerializer(waypointtime)
        return Response(serializer.data)


class RouteDetail(APIView):

    def get_routes(self, **kw):
        day, time, title, stop_id = kw.get('day'), kw.get('time'), kw.get('title'), kw.get('stop_id')
        if title:
            waypoint = Waypoint.objects.filter(stop__title__contains=title)
        elif stop_id:
            waypoint = Waypoint.objects.filter(stop__id=stop_id)
        return WaypointTime.objects.filter(time__gt=time, waypoint__in=waypoint, weekdays=humanized_days_to_flags(day)).order_by('time')

    def get(self, request, **kw):
        routes = self.get_routes(**kw)
        serializer = RouteSerializer(routes)
        return Response(serializer.data)


class StopAndRouteNameDetail(APIView):

    def get_names(self, part_name):
        names = Waypoint.objects.filter(Q(stop__title__contains=part_name) | Q(direction__route__tat_number__contains=part_name) 
            | Q(direction__route__tat_type__title__contains=part_name)).distinct()
        return names.order_by('stop__title')

    def get(self, request, part_name):
        names = self.get_names(part_name)
        serializer = InputSerializer(names)
        return Response(serializer.data)