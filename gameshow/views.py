from django.contrib.auth.models import User

from rest_framework import viewsets

from gameshow import models
from gameshow import serializers


class GameshowViewSet(viewsets.ModelViewSet):
    queryset = models.Gameshow.objects.all()
    serializer_class = serializers.GameshowSerializer
    lookup_field = 'slug'


class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer


class ContestantViewSet(viewsets.ModelViewSet):
    queryset = models.Contestant.objects.all()
    serializer_class = serializers.ContestantSerializer


class UserPredictionViewSet(viewsets.ModelViewSet):
    model = models.UserPrediction
    serializer_class = serializers.UserPredictionSerializer

    def get_queryset(self):
        return models.UserPrediction.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = serializers.UserSerializer
