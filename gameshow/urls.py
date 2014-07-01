from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    '',
    (r'^$', 'gameshow.views.redirect_to_current'),
    (r'^rules/$', 'gameshow.views.rules'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/$', 'gameshow.views.dashboard'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/predictions/(?P<pk>\d+)/$',
        'gameshow.views.prediction_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/past-predictions/$',
        'gameshow.views.past_predictions'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/team/$', 'gameshow.views.team_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/points/$',
        'gameshow.views.points_detail'),
)
