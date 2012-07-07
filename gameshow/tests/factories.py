from datetime import datetime

from django.contrib.auth.models import User
import factory

from gameshow import models

class GameshowFactory(factory.Factory):
    FACTORY_FOR = models.Gameshow

    name = 'My Gameshow'


class EventFactory(factory.Factory):
    FACTORY_FOR = models.Event

    gameshow = factory.SubFactory(GameshowFactory)
    name = 'My Event'
    date = datetime.today()
    date_performed = datetime.today()


class ContestantFactory(factory.Factory):
    FACTORY_FOR = models.Contestant

    gameshow = factory.SubFactory(GameshowFactory)
    name = 'Contestant'
    state = 'active'


class EventContestantFactory(factory.Factory):
    FACTORY_FOR = models.EventContestant

    event = factory.SubFactory(EventFactory)
    contestant = factory.SubFactory(ContestantFactory)


def EventWithContestantsFactory():
    event = EventFactory()
    [EventContestantFactory(event=event) for _ in xrange(3)]
    return event


class PredictionFactory(factory.Factory):
    FACTORY_FOR = models.Prediction

    event = factory.LazyAttribute(lambda a: EventWithContestantsFactory())
    points = 10
    description = 'Predict something'
    number_of_choices = 1
    can_match_team = True


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    first_name = "Test"
    last_name = "User"
    email = "testuser@example.org"
