"""
Tests for models.
"""
# from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


# Helper method to create a user
def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        # Call the create_user method on our user manager for our user model.
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # we verify that that the created user has the right email and password.
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

# what this test does is it just test creating a simple diagnosticTest in the system.
# First we create a user so that we can assign to our diagnosticTest object
# Then we create the diagnosticTest object with its fields
# Lastly we asset that the string representation of the diagnosticTest matches the title of the diagnosticTest object
    def test_create_diagnosticTest(self):
        """Test creating a diagnosticTest is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        diagnosticTest = models.DiagnosticTest.objects.create(
            user=user,
            title='Sample Diagnostic Test Name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample Diagnostic Test description.',
        )

        self.assertEqual(str(diagnosticTest), diagnosticTest.title)

# This test creates a user, creates a tag and assigns it to the user
# it then asserts that the
    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')
# Then we are checking when we convert this tag instance to a string using the str built in function,
# it converts the tag name.
# And the other thing it will test is just that we can simply create new tag instances because if we can't
# create them, we're going to get an error.
        self.assertEqual(str(tag), tag.name)
