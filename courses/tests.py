from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from courses.models import Enrollment, CompletedLesson, TestResult, Course
import json
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def view_profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = get_object_or_404(Profile, user=user)
    total_courses = Enrollment.objects.filter(user=user).count()
    total_lessons = TestResult.objects.filter(user=user, score__gte=70).count()

    courses = Enrollment.objects.filter(user=user).select_related('course')
    course_names = []
    lessons_completed = []
    progress_percentage = []

    for enrollment in courses:
        course = enrollment.course
        completed_lessons = TestResult.objects.filter(user=user, lesson__course=course, score__gte=70).count()
        total_lessons_in_course = course.lessons.count()
        
        course_names.append(course.name)
        lessons_completed.append(completed_lessons)
        progress_percentage.append(
            round((completed_lessons / total_lessons_in_course) * 100, 2) if total_lessons_in_course > 0 else 0
        )

    completed_tests = TestResult.objects.filter(user=user, score__gte=70).order_by('lesson__course', 'lesson', 'passed')
    completed_tests_dates = [test.passed.strftime('%Y-%m-%d') if test.passed else None for test in completed_tests]
    test_scores = [test.score for test in completed_tests]
    lesson_titles = [test.lesson.title for test in completed_tests]

    average_score = TestResult.objects.filter(user=user).aggregate(average_score=json.dumps(sum(test_scores) / len(test_scores) if test_scores else 0))

    context = {
        'profile': profile,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'course_names': json.dumps(course_names),
        'lessons_completed': json.dumps(lessons_completed),
        'progress_percentage': json.dumps(progress_percentage),
        'completed_tests_dates': json.dumps(completed_tests_dates),
        'test_scores': json.dumps(test_scores),
        'lesson_titles': json.dumps(lesson_titles),
        'average_score': average_score['average_score'],
        'is_owner': request.user == user,
    }
    
    return render(request, 'view_profile.html', context)


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('profiles:view_profile')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})


@login_required
def profile_list(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'profile_list.html', {'profiles': profiles})


@login_required
def profile_statistics(request):
    users = User.objects.all()
    statistics = []

    for user in users:
        total_courses = Enrollment.objects.filter(user=user).count()
        total_lessons = TestResult.objects.filter(user=user, score__gte=70).count()
        average_score = TestResult.objects.filter(user=user).aggregate(average_score=json.dumps(sum(TestResult.objects.filter(user=user).values_list('score', flat=True)) / total_lessons if total_lessons else 0))

        statistics.append({
            'username': user.username,
            'total_courses': total_courses,
            'total_lessons': total_lessons,
            'average_score': average_score['average_score'],
        })

    return render(request, 'profile_statistics.html', {'statistics': statistics})
