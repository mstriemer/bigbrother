from django.core.mail import send_mass_mail

from gameshow.models import Gameshow


def send_email_reminders(predictions, users):
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
        mails.append((subject, u'\n'.join(message), sender, [user.email]))
    send_mass_mail(mails)

def old_send_email_reminders():
    gameshow = Gameshow.objects.current()
    preds = [p for e in gameshow.event_set.today()
               for p in e.prediction_set.all()]
    mails = []
    if preds:
        for user in gameshow.users.all():
            body = ['You have the following predictions due today:', '']
            for prediction in preds:
                body.append("* {name}".format(name=prediction))
                for up in prediction.userprediction_set.filter(user=user):
                    for upc in up.userpredictionchoice_set.all():
                        body.append("    * {choice}".format(choice=upc))
                    else:
                        body.append("    * You have not made a prediction")
            mails.append(("Today's predictions",
                          "\n".join(body),
                          "bigbrother@striemer.ca",
                          user.email))
    return mails
