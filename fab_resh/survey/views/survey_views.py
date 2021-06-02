from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, permissions
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
from ..models import Survey, Question, SurveySession, Answer, User
from ..serializers.survey_serializer import (
    GetSurveySerializer,
    CreateSurveySerializer,
    ChangeSurveySerializer,
    GetByIdSurveySerializer,
    GetSurveySessionSerializer,
)

USER_DOES_NOT_EXIST = 'User does not exist'
SURVEY_DOES_NOT_EXIST = 'Survey does not exist'


class CreateSurveyView(AuthView, CreateBaseView):
    '''создание опроса'''
    def __init__(self):
        self.serializer = CreateSurveySerializer

    @swagger_auto_schema(
        tags=['survey'],
        operation_id='create_survey',
        operation_decription='Создание опроса',
        responses={
            '201': CreateSurveySerializer,
            '400': 'bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='активность'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
                'start': openapi.Schema(type=openapi.FORMAT_DATETIME, description='дата старта'),
                'end': openapi.Schema(type=openapi.FORMAT_DATETIME, description='дата конца'),
            }
        )
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class ChangeSurveyView(AuthView, ChangeBaseView):
    '''изменение опроса'''
    def __init__(self):
        self.object = Survey
        self.serializer = ChangeSurveySerializer
        self.DOES_NOT_EXIST_MESSAGE = SURVEY_DOES_NOT_EXIST

    @swagger_auto_schema(
        tags=['survey'],
        operation_id='change_survey',
        operation_decription='Изменение опроса',
        responses={
            '200': ChangeSurveySerializer,
            '400': 'bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='активность'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='имя'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'),
                'end': openapi.Schema(type=openapi.FORMAT_DATETIME, description='дата конца'),
            }
        )
    )
    def patch(self, *args, **kwargs):
        return super().patch(*args, **kwargs)


class DeleteSurveyView(AuthView, DeleteBaseView):
    '''удаление опроса'''
    def __init__(self):
        self.object = Survey
        self.DOES_NOT_EXIST_MESSAGE = SURVEY_DOES_NOT_EXIST

    @swagger_auto_schema(
        tags=['survey'],
        operation_id='delete_survey',
        operation_decription='Удаление опроса',
        responses={
            '200': 'ok',
            '400': 'bad request'
        },
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)


class GetActiveSurveysView(APIView):
    '''получение активных опросов'''
    @swagger_auto_schema(
        tags=['survey'],
        operation_id='get_active_survey',
        operation_decription='Список активных опросов',
        responses={
            '200': 'ok',
        },
    )
    def get(self, request):
        surveys = Survey.objects.filter(is_active=True)
        serializer = GetSurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetSurveyView(APIView):
    '''получение опроса'''
    @swagger_auto_schema(
        tags=['survey'],
        operation_id='get_survey',
        operation_decription='Получение опроса',
        responses={
            '200': GetByIdSurveySerializer,
            '400': 'bad request'
        },
    )
    def get(self, request, id):
        try:
            survey = Survey.objects.get(is_active=True, id=id)
        except ObjectDoesNotExist:
            return Response(
                SURVEY_DOES_NOT_EXIST,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GetByIdSurveySerializer(survey)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RunSurveyView(APIView):
    '''прохождение опроса'''
    def _get_available_question_ids(self, survey):
        return (
            Question.objects
            .filter(survey=survey)
            .values_list('id', flat=True)
        )

    @swagger_auto_schema(
        tags=['survey'],
        operation_id='run_survey',
        operation_decription='Прохождение опроса',
        responses={
            '201': 'survey_id',
            '400': 'bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'answers': openapi.Schema(
                    type=openapi.Items(
                        type='array',
                        items={
                            'question_id':openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
                            'text':openapi.Schema(type=openapi.TYPE_STRING, description='текст ответа'),
                        }
                    )
                )
            }
        )
    )
    def post(self, request, survey_id, user_id):
        answers = request.data.get('answers')
        try:
            survey = Survey.objects.get(id=survey_id, is_active=True)
        except ObjectDoesNotExist:
            return Response(
                SURVEY_DOES_NOT_EXIST,
                status=status.HTTP_400_BAD_REQUEST
            )
        user, _ = User.objects.get_or_create(id=user_id)

        if answers:
            survey_session = SurveySession.objects.create(
                user=user,
                survey=survey
            )
            for answer in answers:
                question = answer.get('question')
                if question in self._get_available_question_ids(survey):
                    question = Question.objects.get(
                        id=question
                    )
                    Answer.objects.create(
                        question=question,
                        text=answer.get('text'),
                        survey_session=survey_session
                    )

        return Response({'user_id': user.id}, status=status.HTTP_200_OK)


class GetUserResultView(APIView):
    '''получение резултатов опросов пользователя'''
    @swagger_auto_schema(
        tags=['survey'],
        operation_id='get_user_result_on_surveys',
        operation_decription='Результаты опросов пользователя',
        responses={
            '200': GetSurveySessionSerializer,
            '400': 'bad request'
        },
    )
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                USER_DOES_NOT_EXIST,
                status=status.HTTP_400_BAD_REQUEST
            )
        survey_sessions = SurveySession.objects.filter(user=user)
        serializer = GetSurveySessionSerializer(survey_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
