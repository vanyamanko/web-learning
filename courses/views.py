# views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Lesson, Question, Answer, CompletedLesson, TestResult
from .forms import EnrollmentForm, LessonForm, QuestionForm
from django.contrib.auth.decorators import login_required
import markdown
import bleach
def courses_list(request):
    courses = Course.objects.all()
    enrollments = {}
    if request.user.is_authenticated:
        enrollments = {enrollment.course_id: enrollment for enrollment in Enrollment.objects.filter(user=request.user)}
    return render(request, 'courses/courses.html', {'courses': courses, 'enrollments': enrollments})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    return render(request, 'courses/course_detail.html', {'course': course, 'enrollment': enrollment})


def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    if Enrollment.objects.filter(user=user, course=course).exists():
        return redirect('course_detail', course_id=course_id)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = user
            enrollment.course = course
            enrollment.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = EnrollmentForm()

    return render(request, 'courses/enroll_course.html', {'form': form, 'course': course})


def lesson_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('title')  # Order lessons by title
    completed_lessons = []
    if request.user.is_authenticated:
        completed_lessons = CompletedLesson.objects.filter(user=request.user, lesson__in=lessons).values_list('lesson_id', flat=True)
    return render(request, 'courses/lesson_list.html', {'course': course, 'lessons': lessons, 'completed_lessons': completed_lessons})

def lesson_detail(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    course = lesson.course
    prev_lesson = Lesson.objects.filter(course=course, id__lt=lesson_id).last()
    next_lesson = Lesson.objects.filter(course=course, id__gt=lesson_id).first()
    completed = False
    passed_test = False
    lesson_content_html = markdown.markdown(lesson.content, extensions=['extra', 'smarty'])
    allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'h3','-', 'strong', 'em', 'ul', 'ol', 'li', 'br', 'hr']
    safe_content = bleach.clean(lesson_content_html, tags=allowed_tags)

    if request.user.is_authenticated:
        completed = CompletedLesson.objects.filter(user=request.user, lesson=lesson).exists()
        test_result = TestResult.objects.filter(user=request.user, lesson=lesson).first()
        if test_result:
            passed_test = test_result.passed

    context = {
        'lesson': lesson,
        'content': safe_content,
        'course': course,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson if passed_test else None,
        'completed': completed,
        'test_result': test_result,
    }
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def mark_lesson_complete(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    CompletedLesson.objects.get_or_create(user=request.user, lesson=lesson)
    return redirect('lesson_detail', course_id=course_id, lesson_id=lesson_id)

@login_required
def lesson_test(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    questions = Question.objects.filter(lesson=lesson)
    question_forms = [
        QuestionForm(question=question, data=request.POST or None, prefix=str(question.id))
        for question in questions
    ]

    if request.method == 'POST':
        total_correct = 0
        for form in question_forms:
            if form.is_valid():
                if form.is_correct():
                    total_correct += 1

        score = (total_correct / questions.count()) * 100 if questions.exists() else 0.0
        passed = score >= 70

        TestResult.save_test_result(
            user=request.user,
            lesson=lesson,
            score=score,
            passed=passed,
            total_correct=total_correct
        )

        next_lesson = Lesson.objects.filter(course=lesson.course, id__gt=lesson_id).first()
        return redirect('lesson_result', course_id=course_id, lesson_id=lesson_id, next_lesson_id=next_lesson.id if next_lesson else 0)

    context = {
        'lesson': lesson,
        'course': lesson.course,
        'question_forms': question_forms,
    }
    return render(request, 'courses/lesson_test.html', context)


@login_required
def lesson_result(request, course_id, lesson_id, next_lesson_id=None):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    test_result = get_object_or_404(TestResult, user=request.user, lesson=lesson)
    next_lesson = None
    if next_lesson_id and next_lesson_id != 0:
        next_lesson = get_object_or_404(Lesson, id=next_lesson_id, course_id=course_id)

    context = {
        'lesson': lesson,
        'course': lesson.course,
        'test_result': test_result,
        'next_lesson': next_lesson,
    }
    return render(request, 'courses/lesson_result.html', context)

@staff_member_required
def add_lesson(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = LessonForm()

    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

import re

def sort_lessons_by_title(lessons):
    def extract_number(lesson):
        match = re.search(r'\d+', lesson.title)
        return int(match.group()) if match else 0

    return sorted(lessons, key=extract_number)

def course_lessons(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    sorted_lessons = sort_lessons_by_title(lessons)
    return render(request, 'courses/course_lessons.html', {'course': course, 'lessons': sorted_lessons})
@login_required
def all_lessons_list(request):
    lessons = Lesson.objects.select_related('course').order_by('course__name', 'id')
    completed_lessons = []
    if request.user.is_authenticated:
        completed_tests = TestResult.objects.filter(user=request.user, score__gte=70).values_list('lesson_id', flat=True)
        completed_lessons = list(completed_tests)
    return render(request, 'courses/all_lessons_list.html', {'lessons': lessons, 'completed_lessons': completed_lessons})

from django.shortcuts import render
from .models import TestResult

@login_required
def all_tests_list(request):
    tests = TestResult.objects.filter(user=request.user).select_related('lesson', 'lesson__course').distinct('lesson_id')
    return render(request, 'courses/all_tests_list.html', {'tests': tests})

