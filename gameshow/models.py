from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

CONTESTANT_STATE_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive')
)


class Gameshow(models.Model):
    """A gameshow."""
    name = models.CharField(max_length=50)
    season = models.IntegerField()

    def __unicode__(self):
        return "%s Season %s" % (self.name, self.season)


class Contestant(models.Model):
    """A contestant on a :model:`gameshow.Gameshow`."""
    gameshow = models.ForeignKey(Gameshow, related_name='contestants')
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=15, choices=CONTESTANT_STATE_CHOICES)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """
    An event on a :model:`gameshow.Gameshow`, has many
    :model"`gameshow.Contestant`s.
    """
    contestants = models.ManyToManyField(Contestant, through='EventContestant',
        related_name='events')
    gameshow = models.ForeignKey(Gameshow, related_name='events')
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now)
    date_performed = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s - %s" % (self.date, self.name)

    def is_complete(self):
        """True if date is in the past and there is a winner."""
        return self.date < datetime.now() and self.winner

    @property
    def winner(self):
        """
        The :model:`gameshow.Contestant` that won the
        :model:`gameshow.Event`.
        """
        try:
            return self.eventcontestant_set.get(place=1).contestant
        except (EventContestant.DoesNotExist, Contestant.DoesNotExist):
            return None


class EventContestant(models.Model):
    """A :model:`gameshow.Contestant` in an :model:`gameshow.Event`."""
    event = models.ForeignKey(Event)
    contestant = models.ForeignKey(Contestant)
    place = models.IntegerField(blank=True, null=True)
    result = models.CharField(blank=True, null=True, max_length=100)


class ContestantResult(models.Model):
    """
    The result of an :model:`gameshow.Event` for a
    :model:`gameshow.Contestant`.
    """
    pass


class Prediction(models.Model):
    """
    A :model:`auth.User`'s prediction of the :model:`gameshow.Result`
    of an event.
    """
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    contestant = models.ForeignKey(Contestant)
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s - %s" % (self.event, self.description)

    def is_editable(self):
        """True if the :model:`gameshow.Prediction` may be edited."""
        return datetime.now() < self.event.date_performed
