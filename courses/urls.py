# urls.py

from django.urls import path
from . import views
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
urlpatterns = [

    path('', views.courses_list, name='courses_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('<int:course_id>/lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/lessons/<int:lesson_id>/test/', views.lesson_test, name='lesson_test'),
    path('<int:course_id>/lessons/<int:lesson_id>/result/<int:next_lesson_id>/', views.lesson_result, name='lesson_result'),
    path('<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('<int:course_id>/lessons/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('lessons/', views.all_lessons_list, name='all_lessons_list'),
    path('tests/', views.all_tests_list, name='all_tests_list'),
    path('<int:course_id>/lessons/<int:lesson_id>/test/', views.lesson_test, name='lesson_test'),
    path('<int:course_id>/lessons/<int:lesson_id>/result/<int:next_lesson_id>/', views.lesson_result, name='lesson_result'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
]
