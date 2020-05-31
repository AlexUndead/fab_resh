from django import forms
from .models import Survey, Question, Answer


class SurveyForm(forms.ModelForm):
    """форма редактирования и просмотра опроса"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Survey
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    """форма редактирования и просмотра вопроса"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Question
        fields = '__all__'


class AnswerForm(forms.ModelForm):
    """форма редактирования и просмотра ответа"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Answer
        fields = '__all__'
