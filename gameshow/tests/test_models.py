from datetime import datetime, timedelta

from django.test import TestCase

from gameshow.models import UserPredictionChoice
from .factories import (GameshowFactory, EventFactory, PredictionFactory,
        UserFactory)

class GameshowTest(TestCase):
    def test_todays_predictions_are_found(self):
        today = datetime.today()
        # set the hour to 0 if 1, 1 if 0, etc
        today = today.replace(hour=int(not today.hour))
        tomorrow = today + timedelta(days=1)
        gameshow = GameshowFactory()
        event1 = EventFactory(gameshow=gameshow, date=today,
                date_performed=today)
        event2 = EventFactory(gameshow=gameshow, date=tomorrow,
                date_performed=tomorrow)
        prediction1 = PredictionFactory(event=event1)
        prediction2 = PredictionFactory(event=event1)
        PredictionFactory(event=event2)
        self.assertEqual([prediction1, prediction2],
                list(gameshow.todays_predictions()))


class PredictionTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        PredictionFactory()
        self.prediction = PredictionFactory()
        self.contestants = self.prediction.event.eventcontestant_set.all()[0:2]
        self.user1_prediction = self.prediction.userprediction_set.create(
                user=self.user1)
        self.choices = [UserPredictionChoice.objects.create(
            user_prediction=self.user1_prediction, event_contestant=contestant)
            for contestant in self.contestants]

    def test_user_choices_are_found(self):
        self.assertEqual(self.choices,
                list(self.prediction.user_choices(self.user1)))

    def test_user_choices_are_not_found(self):
        self.assertEqual([], list(self.prediction.user_choices(self.user2)))
