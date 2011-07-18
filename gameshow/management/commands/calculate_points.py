from django.core.management import BaseCommand, CommandError
from django.contrib.auth.models import User

from gameshow.models import Gameshow, Event, Contestant, EventContestant, \
                            Prediction, UserPrediction


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for gameshow in Gameshow.objects.all():
            self.stdout.write("Points for {0}\n".format(gameshow))
            self.stdout.write("Player     Points\n")
            user_points = gameshow.calculate_points().items()
            user_points.sort(key=lambda up: up[1], reverse=True)
            for user, points in user_points:
                self.stdout.write("{0} {1}\n".format(
                    str(user).ljust(10), points))
