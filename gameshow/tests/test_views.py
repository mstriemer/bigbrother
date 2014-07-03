from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

import mock

from gameshow.views import IsOwner


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
