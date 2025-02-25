from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_profile_fields(self):
        self.assertEqual(self.profile.bio, 'Test bio')


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_detail_view_status_code(self):
        url = reverse('profile_detail', args=[self.profile.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_view_contains_username(self):
        url = reverse('profile_detail', args=[self.profile.pk])
        response = self.client.get(url)
        self.assertContains(response, self.user.username)


class ProfileEditViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_edit_view_redirect_if_not_logged_in(self):
        url = reverse('profile_edit', args=[self.profile.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('profile_edit', args=[self.profile.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bio')
