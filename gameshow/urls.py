from django.conf.urls import patterns, url, include

from rest_framework import routers

from gameshow import views

router = routers.DefaultRouter()
router.register('gameshows', views.GameshowViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
)
