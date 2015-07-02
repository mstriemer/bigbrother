from base64 import b64encode

import mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient, force_authenticate

from gameshow.models import Event, Gameshow
from gameshow.views import IsOwner, EventViewSet


class IsOwnerTestCase(TestCase):
    def make_user(self, **kwargs):
        kwargs.setdefault('first_name', 'Bob')
        return User(**kwargs)

    def make_request(self):
        factory = RequestFactory()
        return factory.get('/api/teams/1/')

    def test_owner_is_allowed(self):
        user = self.make_user()
        obj = mock.Mock()
        obj.user = user
        request = self.make_request()
        request.user = user
        self.assertEqual(
            IsOwner().has_object_permission(request, 'myview', obj),
            True)

    def test_non_owner_is_not_allowed(self):
        user = self.make_user(first_name='Jane', pk=1)
        obj = mock.Mock()
        obj.user = self.make_user(first_name='Joe', pk=2)
        request = self.make_request()
        request.user = user
        self.assertEqual(
            IsOwner().has_object_permission(request, 'myview', obj),
            False)

    def test_no_user_is_not_allowed(self):
        obj = mock.Mock()
        obj.user = self.make_user()
        request = self.make_request()
        request.user = None
        self.assertEqual(
            IsOwner().has_object_permission(request, 'myview', obj),
            False)


class EventViewSetTestCase(TestCase):
    fixtures = ['gameshow-basic', 'admin-user']

    def create(self, data):
        client = APIClient()
        assert client.login(username='mark', password='mark'), 'login'
        return client.post('/api/events/', data, format='json')

    def test_event_is_created_with_contestants(self):
        data = {
            'gameshow': 1,
            'name': 'Head of Household',
            'date': '2015-07-01T12:00:00',
            'date_performed': '2015-07-01T12:00:00',
        }
        initial = Event.objects.count()
        response = self.create(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), initial + 1)
        event = Event.objects.get(pk=response.data['id'])
        gameshow = Gameshow.objects.get(pk=data['gameshow'])
        active_contestants = gameshow.contestant_set.filter(state='active')
        self.assertEqual(event.contestants.count(),
                         active_contestants.count())
