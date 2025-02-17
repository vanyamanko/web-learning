from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import render
from .models import Profile
from courses.models import Enrollment, CompletedLesson, TestResult
from django.utils.dateparse import parse_datetime
import json


@login_required
def available_tests(request):
    courses = Enrollment.objects.filter(user=request.user).select_related('course')
    tests = Test.objects.filter(course__in=[enrollment.course for enrollment in courses])

    context = {
        'tests': tests,
    }
    return render(request, 'available_tests.html', context)


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            score = form.calculate_score()  # Предполагается, что метод calculate_score() существует
            TestResult.objects.create(user=request.user, test=test, score=score)
            return redirect('profiles:view_profile')
    else:
        form = TestForm(test=test)

    context = {
        'form': form,
        'test': test,
    }
    return render(request, 'take_test.html', context)

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    results = TestResult.objects.filter(test=test, user=request.user).order_by('-passed_at')

    context = {
        'test': test,
        'results': results,
    }
    return render(request, 'test_detail.html', context)


@login_required
def test_results(request):
    results = TestResult.objects.filter(user=request.user).select_related('test')

    context = {
        'results': results,
    }
    return render(request, 'test_results.html', context)