import json

import mock
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from gameshow.models import Event
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
    fixtures = ['gameshow-basic']

    def create(self, data):
        return self.client.post('/api/events/', json.dumps(data),
                                content_type='application/json')

    def test_event_is_created(self):
        data = {
            'gameshow': 'bb1',
            'name': 'Head of Household',
        }
        initial = Event.objects.count()
        response = self.create(data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), initial + 1)
