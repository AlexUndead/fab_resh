from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .base_views import (
    AuthView,
    CreateBaseView,
    ChangeBaseView,
    DeleteBaseView,
)
from ..models import Question
from ..serializers.question_serializer import (
    BaseQuestionSerializer,
    CreateQuestionSerializer,
    ChangeQuestionSerializer
)

QUESTION_DOES_NOT_EXIST = 'Question does not exist'


class CreateQuestionView(AuthView, CreateBaseView):
    '''создание вопроса'''
    def __init__(self):
        self.serializer = CreateQuestionSerializer

    @swagger_auto_schema(
        tags=['question'],
        operation_id='create_question',
        operation_decription='Создание вопроса',
        responses={
            '201': CreateQuestionSerializer,
            '400': 'bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='текст'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип'),
                'survey':openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
            }
        )
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class ChangeQuestionView(AuthView, ChangeBaseView):
    '''изменение вопроса'''
    def __init__(self):
        self.object = Question
        self.serializer = ChangeQuestionSerializer
        self.DOES_NOT_EXIST_MESSAGE = QUESTION_DOES_NOT_EXIST

    @swagger_auto_schema(
        tags=['question'],
        operation_id='change_question',
        operation_decription='Изменение вопроса',
        responses={
            '200': ChangeQuestionSerializer,
            '400': 'bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='текст'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='тип'),
                'survey':openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
            }
        )
    )
    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)


class DeleteQuestionView(AuthView, DeleteBaseView):
    '''удаление вопроса'''
    def __init__(self):
        self.object = Question
        self.DOES_NOT_EXIST_MESSAGE = QUESTION_DOES_NOT_EXIST

    @swagger_auto_schema(
        tags=['question'],
        operation_id='delete_question',
        operation_decription='Удаление вопроса',
        responses={
            '200': 'ok',
            '400': 'bad request'
        },
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)
