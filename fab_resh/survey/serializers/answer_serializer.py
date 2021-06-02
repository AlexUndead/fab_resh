from rest_framework import serializers

from ..models import Answer


class GetAnswerSerializer(serializers.ModelSerializer):
    '''сериализатор ответов'''
    question = serializers.CharField(source='question.text')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'text']
