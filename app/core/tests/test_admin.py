"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for the Django admin."""

    # Going to run before every test that is added
    def setUp(self):
        """Create a user and a client."""
        # The Django test client that allows to make HTTP requests
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # Forces authentication for the user on the client
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # Generate the URL for the user list page in the admin
        url = reverse('admin:core_user_changelist')
        # Make a GET request to the URL
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that the edit user page works."""
        # Generate the URL for the user edit page in the admin
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Verify that the response status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works."""
        # Generate the URL for the user creation page in the admin
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
