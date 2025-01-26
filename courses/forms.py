from django import forms
from .models import Enrollment, Lesson, Question, Answer

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = []

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']

class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        prefix = kwargs.pop('prefix', None)
        super().__init__(*args, prefix=prefix, **kwargs)
        self.fields['answers'] = forms.ModelMultipleChoiceField(
            queryset=question.answers.all(),
            widget=forms.CheckboxSelectMultiple,
            label=''
        )
        self.question = question

    def clean_answers(self):
        answers = self.cleaned_data['answers']
        if not answers:
            raise forms.ValidationError("Please select at least one answer.")
        return answers

    def is_correct(self):
        correct_answers = self.question.answers.filter(is_correct=True)
        selected_answers = self.cleaned_data['answers']
        return set(correct_answers) == set(selected_answers)
