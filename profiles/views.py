from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import render
from .models import Profile
from courses.models import Enrollment, CompletedLesson, TestResult
from django.utils.dateparse import parse_datetime
import json
@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    total_courses = Enrollment.objects.filter(user=request.user).count()
    total_lessons = TestResult.objects.filter(user=request.user, score__gte=70).count()

    # Data for charts
    courses = Enrollment.objects.filter(user=request.user).select_related('course')
    course_names = [enrollment.course.name for enrollment in courses]
    lessons_completed = [
        TestResult.objects.filter(user=request.user, lesson__course=enrollment.course, score__gte=70).count()
        for enrollment in courses
    ]

    # Data for timeline chart
    completed_tests = TestResult.objects.filter(user=request.user, score__gte=70).order_by('lesson__course', 'lesson', 'passed')
    completed_tests_dates = [test.passed for test in completed_tests]
    test_scores = [test.score for test in completed_tests]
    lesson_titles = [test.lesson.title for test in completed_tests]

    context = {
        'profile': profile,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'course_names': json.dumps(course_names),
        'lessons_completed': json.dumps(lessons_completed),
        'completed_tests_dates': json.dumps(completed_tests_dates),
        'test_scores': json.dumps(test_scores),
        'lesson_titles': json.dumps(lesson_titles),
    }
    return render(request, 'view_profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})