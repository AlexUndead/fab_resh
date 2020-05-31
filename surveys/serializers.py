from rest_framework import serializers
from .models import Result


class SurveyResultSerialize(serializers.ModelSerializer):
    """Сериализатор результата прохождения опроса"""

    class Meta:
        model = Result
        fields = '__all__'