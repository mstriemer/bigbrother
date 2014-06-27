import string
from random import choice

from django.core.mail import send_mass_mail, send_mail

from datetime import timedelta, datetime, date

from gameshow.models import Gameshow, EventContestant

event_schedule = {}


def send_prediction_reminder_emails(predictions, users):
    if not predictions:
        return
    mails = []
    subject = u"[Big Brother] Today's Predictions"
    sender = u'bigbrother@striemer.ca'
    for user in users:
        if not user.email:
            continue
        message = [u'The following predictions are due today on '
                   'http://bigbrother.striemer.ca:', u'']
        for prediction in predictions:
            message.append(u'* {name}'.format(name=prediction))
            choices = prediction.user_choices(user)
            for i in xrange(prediction.number_of_choices):
                if i < len(choices):
                    message.append(u'    {i}. {choice}'.format(
                                   choice=choices[i], i=i + 1))
                else:
                    message.append(
                        u'    {i}. You have not made a prediction'.format(
                            i=i + 1))
            message.append(u'')
        mails.append((subject, u'\n'.join(message), sender, [user.email]))
    send_mass_mail(mails)


def notify_users_of_todays_predictions():
    gameshow = Gameshow.objects.current()
    predictions = gameshow.todays_predictions()
    users = gameshow.users.all()
    send_prediction_reminder_emails(predictions, users)


def reset_user_password(user):
    letters = string.letters + string.digits
    password = ''.join(choice(letters) for _ in xrange(13))
    user.set_password(password)
    user.save()
    return password


def send_password_info(user):
    password = reset_user_password(user)
    body = u'''
    Hi {first_name},

    Your password has been reset and you can now login with:

        * Username: {username}
        * Password: {password}

    See you at https://bb-pool.herokuapp.com and good luck!
    '''.format(first_name=user.first_name, username=user.username,
               password=password)
    return send_mail(
        u'[Big Brother] Your Password',
        body,
        u'bigbrother@striemer.ca',
        [user.email]
    )


def send_all_password_info():
    gameshow = Gameshow.objects.current()
    users = gameshow.users.all()
    for user in users:
        send_password_info(user)


def create_events_for_tomorrow():
    tomorrow = date.today() + timedelta(days=1)
    create_events_for_date(tomorrow)


def create_events_for_date(event_date, due_date=None):
    url_format = 'https://bb-pool.herokuapp.com/admin/gameshow/event/{pk}/'
    events = event_schedule.get(event_date.strftime('%A'))
    if due_date is None:
        due_date = date.today() + timedelta(days=1)
    if events is not None:
        body = 'The following events were created:\n\n'
        gameshow = Gameshow.objects.current()
        contestants = gameshow.contestant_set.filter(state='active').all()
        for event_data in events:
            day_offset = timedelta(days=event_data.get('day_offset', 0))
            due_datetime = datetime.combine(due_date + day_offset,
                                            event_data['time'])
            event_datetime = datetime.combine(event_date + day_offset,
                                              event_data['time'])
            event = gameshow.event_set.create(
                name=event_data['name'],
                date=event_datetime,
                date_performed=due_datetime,
            )
            for contestant in contestants:
                EventContestant.objects.create(event=event,
                                               contestant=contestant)
            event.prediction_set.create(
                points=event_data['points'],
                description=event_data['description'],
                number_of_choices=event_data['number_of_choices'],
                can_match_team=event_data['can_match_team'],
            )
            body += '    * {name} ({url})\n'.format(
                name=event,
                url=url_format.format(pk=event.pk),
            )
        send_mail(
            u'[Big Brother] Events Created',
            body,
            u'bigbrother@striemer.ca',
            ['mstriemer@gmail.com']
        )
