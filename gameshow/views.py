from rest_framework import viewsets

from gameshow.models import Gameshow, Event
from gameshow.serializers import GameshowSerializer, EventSerializer


class GameshowViewSet(viewsets.ModelViewSet):
    queryset = Gameshow.objects.all()
    serializer_class = GameshowSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
