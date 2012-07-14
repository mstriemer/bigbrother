from datetime import datetime, date, time

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

CONTESTANT_STATE_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive')
)


class GameshowManager(models.Manager):
    def current(self):
        return self.get_query_set().get(pk=2)


class Gameshow(models.Model):
    """A gameshow."""
    objects = GameshowManager()

    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    @property
    def prediction_set(self):
        return Prediction.objects.filter(event__gameshow__pk=self.pk)

    def calculate_points(self):
        user_points = dict([(u, 0) for u in self.users.all()])
        for event in self.event_set.all():
            for prediction in event.prediction_set.all():
                for match in prediction.matching_user_predictions.all():
                    user_points[match.user] += match.prediction.points
                for team in prediction.matching_teams:
                    user_points[team.user] += prediction.points / 2
        return user_points

    def todays_predictions(self):
        return [p for e in self.event_set.today()
                    for p in e.prediction_set.all()]


class Contestant(models.Model):
    """A contestant on a :model:`gameshow.Gameshow`."""
    gameshow = models.ForeignKey(Gameshow)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=15, choices=CONTESTANT_STATE_CHOICES)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def is_active(self):
        return self.state == 'active'


class EventManager(models.Manager):
    def today(self):
        return self.get_query_set().filter(
                date__gte=datetime.combine(date.today(), time.min),
                date__lte=datetime.combine(date.today(), time.max))


class Event(models.Model):
    """
    An event on a :model:`gameshow.Gameshow`, has many
    :model"`gameshow.Contestant`s.
    """
    gameshow = models.ForeignKey(Gameshow)
    contestants = models.ManyToManyField(Contestant, through='EventContestant')
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now)
    date_performed = models.DateTimeField(default=datetime.now)

    objects = EventManager()

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.date)


class EventContestant(models.Model):
    """A :model:`gameshow.Contestant` in an :model:`gameshow.Event`."""
    event = models.ForeignKey(Event)
    contestant = models.ForeignKey(Contestant)
    result = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.contestant)


class Prediction(models.Model):
    """
    A result that may be predicted by a :model:`auth.User`.
    """
    event = models.ForeignKey(Event)
    points = models.IntegerField()
    description = models.CharField(max_length=100)
    matches = models.ManyToManyField('EventContestant',
        through='PredictionMatch')
    number_of_choices = models.IntegerField()
    can_match_team = models.BooleanField()

    def __unicode__(self):
        return "{0} - {1}".format(self.event, self.description)

    @property
    def is_editable(self):
        """True if the :model:`gameshow.Prediction` may be edited."""
        return datetime.now() < self.event.date_performed

    @property
    def matching_user_predictions(self):
        return self.userprediction_set.filter(
            userpredictionchoice__event_contestant__in=self.matches.all())

    @property
    def matching_teams(self):
        if self.can_match_team:
            return Team.objects.filter(teammembership__contestant__in=map(
                lambda ec: ec.contestant_id, self.matches.all()))
        else:
            # Return an empty QuerySet
            return Team.objects.none()

    @property
    def contestants(self):
        return [m.contestant for m in self.matches.all()]

    @property
    def team_match_points(self):
        return self.points / 2 if self.can_match_team else 0

    def user_choices(self, user):
        try:
            return (self.userprediction_set.get(user=user).
                    userpredictionchoice_set.all())
        except UserPrediction.DoesNotExist:
            return []

class PredictionMatch(models.Model):
    prediction = models.ForeignKey(Prediction)
    event_contestant = models.ForeignKey(EventContestant)


class UserPrediction(models.Model):
    """
    The :model:`gameshow.EventContestant` that a :model:`auth.User` predicts
    will match an :model:`gameshow.Prediction`.
    """
    user = models.ForeignKey(User)
    prediction = models.ForeignKey(Prediction)
    event_contestants = models.ManyToManyField(EventContestant,
            through='UserPredictionChoice')

    def __unicode__(self):
        return '{0}: {1}'.format(self.user, self.prediction)

    @property
    def is_editable(self):
        return self.prediction.is_editable

    @property
    def choices(self):
        return self.event_contestants.all()

    def total_points(self):
        points = 0
        matches = [m.contestant for m in self.prediction.matches.all()]
        for event_contestant in self.event_contestants.all():
            if event_contestant.contestant in matches:
                points += self.prediction.points
        try:
            if self.prediction.can_match_team:
                for teammate in Team.objects.get(
                        gameshow=self.prediction.event.gameshow, user=self.user
                        ).contestants.all():
                    if teammate in matches:
                        points += self.prediction.team_match_points
        except Team.DoesNotExist:
            pass
        return points

    def as_form(self, data=None):
        FormSet = inlineformset_factory(UserPrediction,
            UserPredictionChoice, can_delete=False,
            extra=self.prediction.number_of_choices,
            max_num=self.prediction.number_of_choices)
        form_set = FormSet(data, instance=self)
        for form in form_set:
            form.fields['event_contestant'].queryset = \
                self.prediction.event.eventcontestant_set.all().order_by('contestant__name')
            form.fields['event_contestant'].label = 'Contestant'
        return form_set


class UserPredictionChoice(models.Model):
    """
    The :model:`gameshow.EventContestant` that a :model:`User` thinks will
    match a :model:`gameshow.Prediction`.
    """
    user_prediction = models.ForeignKey(UserPrediction)
    event_contestant = models.ForeignKey(EventContestant)

    def __unicode__(self):
        return unicode(self.event_contestant)


class Team(models.Model):
    """
    A :model:`auth.User`'s team of :model:`gameshow.Contestant`s.
    """
    user = models.ForeignKey(User)
    contestants = models.ManyToManyField(Contestant, through='TeamMembership')
    gameshow = models.ForeignKey(Gameshow)

    @property
    def is_editable(self):
        return datetime.now() < datetime(year=2012, month=7, day=22, hour=19,
                minute=0, second=0)


class TeamMembership(models.Model):
    """
    A :model:`gameshow.Contestant`s participation in a :model:`auth.User`s
    :model:`gameshow.Team`.
    """
    team = models.ForeignKey(Team)
    contestant = models.ForeignKey(Contestant)
