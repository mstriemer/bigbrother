from django.core.mail import send_mass_mail

from gameshow.models import Gameshow


def send_prediction_reminder_emails(predictions, users):
    if not predictions:
        return
    mails = []
    subject = u"[Big Brother] Today's Predictions"
    sender = u'bigbrother@striemer.ca'
    for user in users:
        message = [u'The following predictions are due today:', u'']
        for prediction in predictions:
            message.append(u'* {name} (pick {nchoices})'.format(
                name=prediction, nchoices=prediction.number_of_choices))
            for i, choice in enumerate(prediction.user_choices(user)):
                message.append(u'    {i}. {choice}'.format(choice=choice, i=i))
            else:
                message.append(u'    * You have not made a prediction')
            message.append(u'')
        mails.append((subject, u'\n'.join(message), sender, [user.email]))
    send_mass_mail(mails)

def notify_users_of_todays_predictions():
    gameshow = Gameshow.objects.current()
    predictions = gameshow.todays_predictions()
    users = gameshow.users.all()
    send_prediction_reminder_emails(predictions, users)
