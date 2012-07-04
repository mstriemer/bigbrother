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
