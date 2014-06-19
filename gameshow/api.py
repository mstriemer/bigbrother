from django.contrib.auth.models import User

from rest_framework import viewsets, serializers
from rest_framework.decorators import link
from rest_framework.response import Response

from gameshow.models import Contestant, Gameshow, Prediction


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


class ContestantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contestant


class PredictionSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField()
    date_aired = serializers.DateTimeField()
    date_performed = serializers.DateTimeField()
    contestants = ContestantSerializer(many=True)

    class Meta:
        model = Prediction
        fields = [
            'name',
            'description',
            'points',
            'date_aired',
            'date_performed',
            'contestants',
            'matches',
            'number_of_choices',
            'can_match_team',
        ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameshowViewSet(viewsets.ModelViewSet):
    queryset = Gameshow.objects.all()
    serializer_class = GameshowSerializer


class ContestantViewSet(viewsets.ModelViewSet):
    model = Contestant


class PredictionViewSet(viewsets.ModelViewSet):
    model = Prediction
    serializer_class = PredictionSerializer

    @link()
    def mine(self, request, pk=None, gameshow_pk=None):
        prediction = Prediction.objects.get(
            pk=pk, event__gameshow_id=gameshow_pk)
        contestants = [up.contestant
                       for up in prediction.userprediction_set.filter(
                           user=request.user.pk)]
        serializer = ContestantSerializer(contestants, many=True)
        return Response(serializer.data)


class GameshowPredictionViewSet(viewsets.ModelViewSet):
    model = Prediction
    serializer_class = PredictionSerializer

    def list(self, request, gameshow_pk):
        self.queryset = (Prediction.objects
                                   .filter(event__gameshow_id=gameshow_pk)
                                   .order_by('-event__date_performed',
                                             '-event__date'))
        return super(GameshowPredictionViewSet, self).list(request)
