import string
from random import choice

from django.core.mail import send_mass_mail, send_mail

from gameshow.models import Gameshow


def send_prediction_reminder_emails(predictions, users):
    if not predictions:
        return
    mails = []
    subject = u"[Big Brother] Today's Predictions"
    sender = u'bigbrother@striemer.ca'
    for user in users:
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

    See you at http://bigbrother.striemer.ca and good luck!
    '''.format(first_name=user.first_name, username=user.username,
            password=password)
    return send_mail(u'[Big Brother] Your Password', body, u'bigbrother@striemer.ca',
            [user.email])

def send_all_password_info():
    gameshow = Gameshow.objects.current()
    users = gameshow.users.all()
    for user in users:
        send_password_info(user)
