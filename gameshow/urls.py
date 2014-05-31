from django.conf.urls.defaults import include, patterns
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from rest_framework import viewsets, routers, serializers

from gameshow.models import Contestant, Gameshow


class GameshowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gameshow
        fields = [
            'name',
            'slug',
            'teams_editable_before',
            'url',
            'users',
            'contestant_set',
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'date_joined',
            'email',
            'first_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_name',
            'url',
            'username',
        ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameshowViewSet(viewsets.ModelViewSet):
    queryset = Gameshow.objects.all()
    serializer_class = GameshowSerializer


class ContestantViewSet(viewsets.ModelViewSet):
    model = Contestant

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('gameshows', GameshowViewSet)
router.register('contestants', ContestantViewSet)

def two(request):
    return render_to_response('gameshow/two.html')

urlpatterns = patterns('',
    (r'^$', 'gameshow.views.redirect_to_current'),
    (r'^two/', two),
    (r'^api/', include(router.urls)),
    (r'^rules/$', 'gameshow.views.rules'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/$', 'gameshow.views.dashboard'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/predictions/(?P<pk>\d+)/$', 'gameshow.views.prediction_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/past-predictions/$', 'gameshow.views.past_predictions'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/team/$', 'gameshow.views.team_detail'),
    (r'^(?P<gameshow_slug>[a-z0-9-]+)/points/$', 'gameshow.views.points_detail'),
)
