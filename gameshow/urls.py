from django.conf.urls.defaults import patterns, include

from rest_framework import routers

from gameshow import views

router = routers.DefaultRouter()
router.register('events', views.EventViewSet)
router.register('gameshows', views.GameshowViewSet)
router.register('users', views.UserViewSet)
router.register('teams', views.TeamViewSet)
router.register('contestants', views.ContestantViewSet)

urlpatterns = patterns(
    '',
    (r'^api/', include(router.urls)),
    ('r^new/', 'gameshow.views.new'),
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
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/graphs/$',
        'gameshow.views.graph'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/events/new/$',
        'gameshow.views.new_event'),
)
