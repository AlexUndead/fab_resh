from rest_framework import serializers
from .models import Result


class SurveyResultSerialize(serializers.ModelSerializer):
    """Сериализатор результата прохождения опроса"""
    result = serializers.JSONField()
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Result
        fields = ('result', 'user_id', 'slug')
