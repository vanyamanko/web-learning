# urls.py

from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
urlpatterns = [

    path('', views.tests_list, name='tests_list'),
    path('<int:tests_id>/', views.tests_detail, name='tests_detail'),
    path('<int:tests_id>/enroll/', views.tests_course, name='enroll_tests'),
    path('<int:tests_id>/lessons/', views.lesson_tests_list, name='lesson_tests'),

    path('', views.available_tests, name='available_tests'),
    path('<int:test_id>/', views.test_detail, name='test_detail'),
    path('<int:test_id>/take/', views.take_test, name='take_test'),
    path('<int:test_id>/results/', views.test_results, name='test_results'),
    path('<int:test_id>/retake/', views.retake_test, name='retake_test'),
]
