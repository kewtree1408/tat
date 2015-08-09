from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test', views.test_backbone, name='test'),
    url(r'^route_suggest', views.route_suggest, name='route_suggest'),
    url(r'^stop_suggest', views.stop_suggest, name='stop_suggest'),
    url(r'^(?P<idx>[0-9]+)$', views.times, name='times'),
)
