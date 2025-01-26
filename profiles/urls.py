from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'profiles'

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    # Other URL patterns for the profile app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
