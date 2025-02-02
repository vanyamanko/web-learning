from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Profile

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        # Создаём тестового пользователя и профиль
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_str(self):
        """Метод __str__ модели Profile должен возвращать имя пользователя."""
        self.assertEqual(str(self.profile), self.user.username)

    def test_profile_fields(self):
        """Проверяем, что поле bio заполнено корректно."""
        self.assertEqual(self.profile.bio, 'Test bio')


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        # Создаём тестового пользователя и профиль
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_detail_view_status_code(self):
        """
        Проверяем, что при запросе детальной страницы профиля возвращается статус 200.
        Предполагается, что URL построен по схеме: name='profile_detail' с параметром pk.
        """
        url = reverse('profile_detail', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_view_contains_username(self):
        """Проверяем, что страница деталей профиля содержит имя пользователя."""
        url = reverse('profile_detail', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertContains(response, self.user.username)


class ProfileEditViewTest(TestCase):
    def setUp(self):
        # Создаём тестового пользователя и профиль
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_edit_view_redirect_if_not_logged_in(self):
        """
        Если пользователь не авторизован, то доступ к странице редактирования должен
        перенаправлять на страницу логина.
        Предполагается, что URL для редактирования профиля называется 'profile_edit'.
        """
        url = reverse('profile_edit')
        response = self.client.get(url)
        # В стандартном случае редирект на страницу логина имеет статус 302
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_view_logged_in(self):
        """
        Авторизованный пользователь должен иметь доступ к странице редактирования профиля.
        """
        self.client.login(username='testuser', password='12345')
        url = reverse('profile_edit')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Можно также проверить, что форма содержит необходимые поля, например bio.
        self.assertContains(response, 'bio')
