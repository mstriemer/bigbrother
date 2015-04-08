from django.core.management.base import BaseCommand

from datetime import date, timedelta

from gameshow.tasks import create_events_for_date, event_schedule


class Command(BaseCommand):
    help = 'Create events for the next show night.'

    def handle(self, day_to_create_events, *args, **options):
        today = date.today()
        if today.strftime('%A') != day_to_create_events:
            print("Not creating any events today.")
            return
        else:
            print("Today's the day, creating events.")
        has_show = lambda day: day.strftime('%A') in event_schedule
        next_week = [today + timedelta(days=i) for i in range(1, 8)]
        show_days = [day for day in next_week if has_show(day)]
        for day, last_show in zip(show_days, [today] + show_days):
            create_events_for_date(day, due_date=last_show + timedelta(days=1))
