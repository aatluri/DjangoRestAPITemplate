"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        # Used to make http requests
        self.client = Client()
        # create an admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # force authentication using the above created user.
        self.client.force_login(self.admin_user)
        # create a regular user.
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        # gives us the url for the changelist i.e list of users in the system.
        # Available in the django docs at https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
        url = reverse('admin:core_user_changelist')
        # makes a request to the url. Because we have force login defined, it will login as the admin user.
        res = self.client.get(url)
        # we validate that the name and email address match.
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # get the url for the change user page and then pass the userid using args
        url = reverse('admin:core_user_change', args=[self.user.id])
        # call the url
        res = self.client.get(url)

        # check that we get a success code.
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        # get the url for add user page
        url = reverse('admin:core_user_add')
        # call the url
        res = self.client.get(url)

        # test that we are getting a success status code.
        self.assertEqual(res.status_code, 200)
