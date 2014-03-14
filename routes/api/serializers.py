from django.forms import widgets
from rest_framework import serializers
from core.models import TatType, Stop, Route, Direction, Waypoint, WaypointTime

class StopSerializer(serializers.HyperlinkedModelSerializer):
    direction_title = serializers.Field(source='direction_title')
    stop_title = serializers.Field(source='stop_title')

    class Meta:
        model = Waypoint
        fields = ('id', 'stop_title', 'direction_title')


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WaypointTime
        fields = ('id', 'time')


class TimeWithDirectionSerializer(serializers.HyperlinkedModelSerializer):
    direction_title = serializers.Field(source='direction_title')

    class Meta:
        model = WaypointTime
        fields = ('id', 'time', 'direction_title')


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    route_title = serializers.Field(source='route_title')
    stop_title = serializers.Field(source='stop_title')
    direction_title = serializers.Field(source='direction_title')

    class Meta:
        model = WaypointTime
        fields = ('id', 'time', 'route_title', 'stop_title', 'direction_title')
