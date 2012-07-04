from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User

from gameshow.models import Prediction, UserPredictionChoice
from gameshow.tasks import send_email_reminders

from mock import Mock


class SendEmailRemindersTest(TestCase):
    def setUp(self):
        self.users = [User(email='user1@example.com', first_name='User'),
                      User(email='user2@example.com', first_name='Yooser')]
        self.titles = ['Head of Household', 'Power of Veto']
        self.predictions = []
        for title in self.titles:
            prediction = Mock(spec_set=Prediction())
            prediction.__unicode__ = Mock()
            prediction.__unicode__.return_value = title
            prediction.number_of_choices = 1
            prediction.user_choices = Mock(return_value=[])
            self.predictions.append(prediction)

    def test_users_are_not_emailed_about_nothing(self):
        send_email_reminders([], self.users)
        self.assertEqual(0, len(mail.outbox))

    def test_users_are_emailed_about_something(self):
        send_email_reminders(self.predictions, self.users)
        self.assertEqual(2, len(mail.outbox))
        for i, user in enumerate(self.users):
            self.assertEqual([user.email], mail.outbox[i].recipients())

    def test_users_are_informed_of_predictions(self):
        send_email_reminders(self.predictions, self.users)
        for title in self.titles:
            for email in mail.outbox:
                self.assertEqual("[Big Brother] Today's Predictions",
                        email.subject)
                self.assertIn(title, email.body)

    def test_emails_are_sent_from_the_right_address(self):
        send_email_reminders(self.predictions, self.users)
        for email in mail.outbox:
            self.assertEqual('bigbrother@striemer.ca', email.from_email)

    def test_users_are_informed_they_havent_chosen(self):
        self.predictions[0].user_choices = Mock(return_value=[])
        send_email_reminders([self.predictions[0]], self.users)
        for email in mail.outbox:
            self.assertIn('You have not made a prediction', email.body)

    def test_users_are_informed_who_they_chose(self):
        name = 'That Person'
        user_choice = Mock(spec_set=UserPredictionChoice)
        user_choice.__unicode__ = lambda self: name
        self.predictions[0].user_choices = Mock(return_value=[user_choice])
        send_email_reminders([self.predictions[0]], [self.users[0]])
        for email in mail.outbox:
            self.assertIn(name, email.body)

    def test_users_are_informed_of_how_many_choices_to_make(self):
        self.predictions[0].number_of_choices = 8128
        send_email_reminders([self.predictions[0]], [self.users[0]])
        for email in mail.outbox:
            self.assertIn(u'{} (pick 8128)'.format(self.titles[0]), email.body)
