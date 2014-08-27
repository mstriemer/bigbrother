from django.conf.urls import patterns, url, include

from rest_framework import routers

from gameshow import views

router = routers.DefaultRouter()
router.register('gameshows', views.GameshowViewSet)
router.register('events', views.EventViewSet)
router.register('contestants', views.ContestantViewSet)
router.register('predictions', views.UserPredictionViewSet)
router.register('users', views.UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
