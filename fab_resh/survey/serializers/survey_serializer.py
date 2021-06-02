from rest_framework import serializers

from .answer_serializer import GetAnswerSerializer
from .question_serializer import BaseQuestionSerializer
from ..models import Survey, SurveySession


class GetSurveySerializer(serializers.ModelSerializer):
    '''базовый сериализатор опроса'''

    class Meta:
        model = Survey
        fields = ['id']


class GetByIdSurveySerializer(serializers.ModelSerializer):
    '''сериализатор просмотра опроса по id'''
    question_set = BaseQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = [
            'id',
            'is_active',
            'name',
            'description',
            'start',
            'end',
            'question_set',
        ]


class CreateSurveySerializer(serializers.ModelSerializer):
    '''сериализатор создания опроса'''
    is_active = serializers.IntegerField(required=False)

    class Meta:
        model = Survey
        fields = "__all__"


class ChangeSurveySerializer(serializers.ModelSerializer):
    '''сериализатор изменения опроса'''
    is_active = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False, max_length=50)
    description = serializers.CharField(required=False, max_length=250)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)

    def validate_start(self, value):
        '''валидация изменения поля "старт"'''
        raise serializers.ValidationError('This field cannot be changed')

    class Meta:
        model = Survey
        fields = "__all__"


class GetSurveySessionSerializer(serializers.ModelSerializer):
    '''сериализатор сессий опроса'''
    answer_set = GetAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = SurveySession
        fields = ['id', 'user', 'survey', 'answer_set']
