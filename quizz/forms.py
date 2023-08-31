from django import forms

from quizz.models import Question, Test
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class QuestionForm(forms.ModelForm):
    question_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Question
        fields = ['text']


class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ['number_of_passing', ' user_answers']


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'answer']
