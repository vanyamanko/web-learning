from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone_number', 'country']
    # Добавьте другие поля, которые вы хотите отобразить в админке