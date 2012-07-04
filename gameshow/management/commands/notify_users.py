from django.core.management.base import BaseCommand

from gameshow.tasks import notify_users_of_todays_predictions

class Command(BaseCommand):
    help = 'Send email notifications about predictions that are due today'

    def handle(self, *args, **options):
        notify_users_of_todays_predictions()
