from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .decorators import auth
from ..views.survey_views import SURVEY_DOES_NOT_EXIST
from ..models import Survey, Question, User as CustomUser, Answer, SurveySession
from ..serializers.survey_serializer import (
    GetSurveySerializer,
    CreateSurveySerializer,
    GetByIdSurveySerializer,
    GetSurveySessionSerializer
)


class SurveyTest(APITestCase):
    '''Тест опроса'''

    def test_get_active_survey(self):
        '''получение активных опросов'''
        url = reverse('survey:get')
        Survey.objects.create(
            is_active=True,
            start=timezone.now(),
            end=timezone.now()
        )
        Survey.objects.create(
            is_active=False,
            start=timezone.now(),
            end=timezone.now()
        )
        active_surveys = Survey.objects.filter(is_active=True)
        serializer = GetSurveySerializer(active_surveys, many=True)
        response = self.client.get(url, format='json')

        self.assertEqual(response.data, serializer.data)

    @auth
    def test_get_survey_result_view(self):
        '''получение результатов опроса'''
        survey = Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )
        Question.objects.create(text='text1', type=1, survey=survey)

        url = reverse('survey:get_by_id', args=[1])
        response = self.client.get(url, format='json')
        serializer = GetByIdSurveySerializer(survey)

        self.assertEqual(response.data, serializer.data)

    def test_get_survey_by_id_view(self):
        '''получение опроса по id'''
        survey = Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )

        url = reverse('survey:get_by_id', args=[1])
        response = self.client.get(url, format='json')
        serializer = GetByIdSurveySerializer(survey)

        self.assertEqual(response.data, serializer.data)

    @auth
    def test_create_survey_view(self):
        '''создания опроса'''
        url = reverse('survey:create')
        response = self.client.post(
            url,
            data={
                'name': 'test',
                'description': 'test_desc',
                'start': timezone.now(),
                'end': timezone.now(),
            },
            format='json'
        )
        survey = Survey.objects.first()
        serializer = CreateSurveySerializer(survey)

        self.assertEqual(response.data, serializer.data)

    @auth
    def test_change_survey_view(self):
        '''изменение опроса'''
        Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )

        url = reverse('survey:change', args=[1])
        response = self.client.patch(
            url,
            data={
                'name': 'test1',
                'description': 'test_desc',
                'end': timezone.now(),
            },
            format='json'
        )

        self.assertEqual(response.data['name'], 'test1')

    @auth
    def test_delete_survey_view(self):
        '''удаление опроса'''
        Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )
        survey = Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )

        url = reverse('survey:delete', args=[1])
        self.client.delete(url, format='json')
        surveys = Survey.objects.all()

        self.assertIn(survey, surveys)

    def test_run_survey_view(self):
        '''прохождение опроса'''
        user = CustomUser.objects.create()
        survey = Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )
        question = Question.objects.create(text='text1', type=1, survey=survey)

        request_body = {
            'answers': [
                {'question_id': question.id, 'text': 'test1'},
            ]
        }
        url = reverse('survey:run', args=[1, 1])
        response = self.client.post(url, data=request_body, format='json')

        self.assertEqual(response.data, {'user_id': user.id})

    def test_get_user_result_view(self):
        '''получение результата опроса'''
        user = CustomUser.objects.create()
        survey = Survey.objects.create(
            name='test',
            description='test_desc',
            start=timezone.now(),
            end=timezone.now(),
        )
        survey_session = SurveySession.objects.create(user=user, survey=survey)
        question = Question.objects.create(text='text1', type=1, survey=survey)
        Answer.objects.create(
            text='text_answer1',
            question=question,
            survey_session=survey_session
        )
        survey_sessions = SurveySession.objects.all()
        serializer = GetSurveySessionSerializer(survey_sessions, many=True)

        url = reverse('survey:get_user_result', args=[1])
        response = self.client.get(url, forma='json')

        self.assertEqual(response.data, serializer.data)

    @auth
    def test_except_survey_does_not_exist(self):
        '''исключение: опроса не существует'''
        cl = self.client
        delete, patch, get = cl.delete, cl.patch, cl.get
        for action in (
            ('change', patch),
            ('delete', delete),
            ('get_by_id', get),
            ('get_user_result', get)
        ):
            name_action, method = action
            url = reverse('survey:' + name_action, args=[1])
            response = method(url, data={}, forma='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @auth
    def test_except_survey_does_not_exist(self):
        '''исключение: опроса не существует'''
        url = reverse('survey:run', args=[1, 1])
        response = self.client.post(url, data={}, forma='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
