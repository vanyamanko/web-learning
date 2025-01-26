from django.contrib import admin
from django.urls import path, include
from users.views import home
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('profile/', include(('profiles.urls', 'profiles'), namespace='profiles')),  # Including profile app routes with namespace
    path('i18n/', include('django.conf.urls.i18n')),  # Adding the i18n URLs for language settings
]

urlpatterns += i18n_patterns(
    path('', home, name='home'),
)
