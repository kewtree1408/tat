# -*- coding:  utf-8 -*-

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views


# input: номер ТАТ, тип ТАТ, название остановки, день недели, текущее время
# output: ближайшие 10 временных значения
# example: /api/title_tat=626_Автобус&stop=Рублево&day=будни&time=13:30

urlpatterns = patterns('core.views',
    (r'^title_tat=(?P<number>.*)_(?P<type>.*)&stop=(?P<stop>.*)&day=(?P<day>.*)&time=(?P<time>.*)$',
        views.TimeDetail.as_view()),
)

# input: день недели, время маршрута и название остановки
# output: название маршрутов, отсортированные по времени, наиболее ближайшему к заданному
# example: /api/day=будни&time=8:30&stop=Катукова

urlpatterns += patterns('core.views',
    (r'^day=(?P<day>.*)&time=(?P<time>.*)&stop=(?P<title>.*)$',
        views.RouteDetail.as_view()),
)

# input: день недели, время маршрута и id остановки
# output: название маршрутов, отсортированные по времени, наиболее ближайшему к заданному
# example: /api/day=будни&time=8:30&stop_id=1303

urlpatterns += patterns('core.views',
    (r'^day=(?P<day>.*)&time=(?P<time>.*)&stop_id=(?P<stop_id>[0-9]+)$',
        views.RouteDetail.as_view()),
)

# input: номер ТАТ, тип ТАТ
# output: остановки, через которые проходит этот ТАТ, сгруппированные по направлению
# exapmle: /api/tat_title=626_Автобус

urlpatterns += patterns('core.views',
    (r'^tat_title=(?P<number>.*)_(?P<type>.*)$',
        views.StopDetail.as_view()),
)

# input: остановка, номер ТАТ, тип ТАТ, день недели
# output: время, сгруппированное по направлению движения
# example: /api/title_tat=626_Автобус&stop=Рублево&day=будни

urlpatterns += patterns('core.views',
    (r'^title_tat=(?P<number>.*)_(?P<type>.*)&stop=(?P<stop>.*)&day=(?P<day>.*)$',
        views.TimeDetail.as_view()),
)


urlpatterns = format_suffix_patterns(urlpatterns)
