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
        # Получаем экземпляр вопроса
        question = kwargs.pop('question')
        prefix = kwargs.pop('prefix', None)
        super().__init__(*args, prefix=prefix, **kwargs)
        # Добавляем поле с вариантами ответа
        self.fields['answers'] = forms.ModelMultipleChoiceField(
            queryset=question.answers.all(),
            widget=forms.CheckboxSelectMultiple,
            label=''
        )
        self.question = question

    def clean_answers(self):
        answers = self.cleaned_data.get('answers')
        if not answers:
            raise forms.ValidationError("Пожалуйста, выберите хотя бы один ответ.")
        return answers

    def clean(self):
        cleaned_data = super().clean()
        answers = cleaned_data.get('answers')

        # Проверка: у вопроса должен быть хотя бы один правильный ответ
        if not self.question.answers.filter(is_correct=True).exists():
            raise forms.ValidationError("Ошибка конфигурации: у этого вопроса не настроен ни один правильный ответ.")

        # Если вопрос позволяет выбрать только один вариант, проверяем, что выбрано не более одного ответа.
        # Предполагается, что у модели Question есть атрибут allow_multiple.
        if hasattr(self.question, 'allow_multiple') and not self.question.allow_multiple:
            if answers and len(answers) > 1:
                raise forms.ValidationError("Для этого вопроса можно выбрать только один ответ.")

        # Здесь можно добавить и другие проверки, если потребуется
        return cleaned_data

    def is_correct(self):
        """
        Метод для проверки правильности выбранных ответов.
        Сравниваем множества правильных ответов и выбранных пользователем.
        """
        correct_answers = self.question.answers.filter(is_correct=True)
        selected_answers = self.cleaned_data.get('answers')
        # Если по каким-то причинам ответы не прошли валидацию, считаем, что ответ неверный.
        if selected_answers is None:
            return False
        return set(correct_answers) == set(selected_answers)
