from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'gameshow.views.dashboard'),
    (r'^predictions/(?P<pk>\d+)/$', 'gameshow.views.prediction_detail'),
    (r'^team/$', 'gameshow.views.team_detail'),
    (r'^rules/$', direct_to_template, {'template':
    'gameshow/bigbrother_rules.html'}),
)
