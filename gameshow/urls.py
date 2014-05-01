from django.conf.urls.defaults import include, patterns
from django.contrib.auth.models import User

from rest_framework import viewsets, routers

from gameshow.models import Contestant, Gameshow


class UserViewSet(viewsets.ModelViewSet):
    model = User


class GameshowViewSet(viewsets.ModelViewSet):
    model = Gameshow
    lookup_field = 'slug'
    lookup_url_kwarg = 'gameshow_slug'


class ContestantViewSet(viewsets.ModelViewSet):
    model = Contestant

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('gameshows', GameshowViewSet)
router.register('contestants', ContestantViewSet)

urlpatterns = patterns('',
    (r'^$', 'gameshow.views.redirect_to_current'),
    (r'^', include(router.urls)),
    (r'^rules/$', 'gameshow.views.rules'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/$', 'gameshow.views.dashboard'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/predictions/(?P<pk>\d+)/$', 'gameshow.views.prediction_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/past-predictions/$', 'gameshow.views.past_predictions'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/team/$', 'gameshow.views.team_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/points/$', 'gameshow.views.points_detail'),
)
