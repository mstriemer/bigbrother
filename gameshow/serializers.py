from django.contrib.auth.models import User

from rest_framework import serializers

from gameshow.models import Gameshow, Event, Contestant, UserPrediction


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'name', 'username']


class GameshowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gameshow
        fields = ['url', 'name', 'slug']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['url', 'gameshow', 'name', 'points', 'number_of_choices',
                  'can_match_team', 'due_at', 'aired_at']


class ContestantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contestant
        fields = ['url', 'gameshow', 'name', 'active']


class UserPredictionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        models = UserPrediction
        fields = ['url', 'event', 'contestant', 'user']
