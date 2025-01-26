# admin.py

from django.contrib import admin
from django.db import IntegrityError
from .models import Course, Lesson, Question, Answer, Enrollment, CompletedLesson
from django.contrib import admin
from django.db import IntegrityError
from .models import Course, Lesson, Question, Answer, Enrollment, CompletedLesson
from django import forms
from django.db import models
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2  # Number of extra forms for new answers

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Number of extra forms for new questions
    show_change_link = True

class LessonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'class': 'vLargeTextField'})},
    }
    inlines = [QuestionInline]

class CourseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except IntegrityError:
            self.message_user(request, "Ошибка сохранения: курс с такими данными уже существует.", level="ERROR")

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Enrollment)
admin.site.register(CompletedLesson)
