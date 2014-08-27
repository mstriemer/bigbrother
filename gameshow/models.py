from django.db import models


class Gameshow(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()


class Event(models.Model):
    gameshow = models.ForeignKey('gameshow.Gameshow')
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    number_of_choices = models.IntegerField()
    can_match_team = models.BooleanField(default=False)
    due_at = models.DateTimeField()
    aired_at = models.DateTimeField()


class Contestant(models.Model):
    gameshow = models.ForeignKey('gameshow.Gameshow')
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)


class UserPrediction(models.Model):
    event = models.ForeignKey('gameshow.Event')
    contestant = models.ForeignKey('gameshow.Contestant')
    user = models.ForeignKey('auth.User')
