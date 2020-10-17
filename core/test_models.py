from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(username='test1', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

    def test_create_user_successful(self):
        """Test creating a new user  successful"""
        username = 'test1'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_username_normalized(self):
        """Test the username for a new user is normalized"""
        username = 'test1'
        user = get_user_model().objects.create_user(username, 'test123')

        self.assertEqual(user.username, username.lower())

    def test_new_user_invalid_username(self):
        """Test creating user with no username raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test1',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


