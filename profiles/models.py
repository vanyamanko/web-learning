# profiles/models.py
from django.db import models
from django.conf import settings
from users.models import CustomUser  # Импортируем вашу кастомную модель пользователя
from django.conf import settings
from django.db import models
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Изменяем связь на вашу кастомную модель пользователя
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Update this line
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    # Другие поля профиля

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'profiles'

