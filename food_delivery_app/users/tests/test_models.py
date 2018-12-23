from django.test import TestCase
from django.contrib.auth import get_user_model

from .factories import UserFactory


User = get_user_model()


class TestUserModel(TestCase):

    def test_create_user(self):
        user = UserFactory.create()
        self.assertIsInstance(user, User)
        self.assertEqual(User.objects.count(), 1)
