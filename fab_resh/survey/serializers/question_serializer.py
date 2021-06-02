from rest_framework import serializers

from ..models import Survey, Question, Answer, TYPE_CHOICES
from ..fields import LabelChoiceField


class BaseQuestionSerializer(serializers.ModelSerializer):
    '''базовый сериализатор вопроса'''
    type = LabelChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = Question
        fields = ['id', 'type', 'text']


class CreateQuestionSerializer(BaseQuestionSerializer):
    '''сериализатор создания вопроса'''

    class Meta:
        model = Question
        fields = ['id', 'type', 'text', 'survey']


class ChangeQuestionSerializer(serializers.ModelSerializer):
    """сериализатор изменения вопроса"""
    text = serializers.CharField(required=False)
    type = LabelChoiceField(required=False, choices=TYPE_CHOICES)
    survey = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Survey.objects.all()
    )

    class Meta:
        model = Question
        fields = "__all__"
