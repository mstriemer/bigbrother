from django.core.management.base import BaseCommand

from datetime import date, timedelta

from gameshow.tasks import create_events_for_date, event_schedule

class Command(BaseCommand):
    help = 'Create events for the next show night.'

    def handle(self, *args, **options):
        today = date.today()
        if today.strftime('%A') not in event_schedule:
            return
        one_day = timedelta(days=1)
        next_show = today + one_day
        while next_show.strftime('%A') not in event_schedule:
            next_show += one_day
        create_events_for_date(next_show)
