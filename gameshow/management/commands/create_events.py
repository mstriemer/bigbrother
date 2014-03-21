from django.core.management.base import BaseCommand

from datetime import date, timedelta

from gameshow.tasks import create_events_for_date, event_schedule

class Command(BaseCommand):
    help = 'Create events for the next show night.'

    def handle(self, day_to_create_events, *args, **options):
        if date.today().strftime('%A') != day_to_create_events:
            print("Not creating any events today.")
            return
        else:
            print("Today's the day, creating events.")
        last_show = date.today()
        one_day = timedelta(days=1)
        has_show = lambda day: day.strftime('%A') in event_schedule
        next_week = [last_show + timedelta(days=i) for i in range(1, 8)]
        show_days = [day for day in next_week if has_show(day)]
        for day in show_days:
            create_events_for_date(day, due_date=last_show + one_day)
            last_show = day
