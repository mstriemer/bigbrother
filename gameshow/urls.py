from django.conf.urls.defaults import include, patterns
from django.shortcuts import render_to_response

from rest_framework import routers

from gameshow.api import (UserViewSet, GameshowViewSet, ContestantViewSet,
                          PredictionViewSet, GameshowPredictionViewSet)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('gameshows', GameshowViewSet)
router.register('contestants', ContestantViewSet)
router.register('predictions', PredictionViewSet)

gameshow_router = routers.DefaultRouter()
gameshow_router.register('predictions', GameshowPredictionViewSet)


def two(request):
    return render_to_response('gameshow/two.html')

urlpatterns = patterns(
    '',
    (r'^$', 'gameshow.views.redirect_to_current'),
    (r'^two/', two),
    (r'^api/', include(router.urls)),
    (r'^api/gameshows/(?P<gameshow_pk>\d+)/', include(gameshow_router.urls)),
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
