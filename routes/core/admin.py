from django.contrib import admin
from .models import TatType, Route, WaypointTime, Waypoint, Direction


admin.site.register(Route)
admin.site.register(TatType)
admin.site.register(WaypointTime)
admin.site.register(Waypoint)
admin.site.register(Direction)

