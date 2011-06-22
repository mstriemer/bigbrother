from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^gameshows/$', 'gameshow.views.gameshow_list'),
    (r'^gameshows/(?P<pk>\d+)/$', 'gameshow.views.gameshow_detail'),
    (r'^contestants/(?P<pk>\d+)/$', 'gameshow.views.contestant_detail'),
    (r'^events/(?P<pk>\d+)/$', 'gameshow.views.event_detail'),
    (r'^predictions/$', 'gameshow.views.prediction_list'),
    (r'^predictions/(?P<pk>\d+)/$', 'gameshow.views.prediction_detail'),
    # (r'^predictions/(?P<year>\d+)/(?P<month>\W+)/(?P<day>\d+)/$',
    #     'gameshow.views.prediction_week_list'),
)
