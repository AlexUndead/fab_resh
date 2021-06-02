from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .decorators import auth
from ..models import Survey, Question, User as CustomUser
from ..serializers.question_serializer import CreateQuestionSerializer


class QuestionTest(APITestCase):
    '''Тест вопросов'''

    @auth
    def test_create_question_view(self):
        '''создание вопроса'''
        Survey.objects.create(
            is_active=True,
            start=timezone.now(),
            end=timezone.now()
        )

        url = reverse('question:create')
        request_body = {
            'text': 'test',
            'type': 'ответ текстом',
            'survey': 1
        }
        response = self.client.post(url, data=request_body, format='json')
        question = Question.objects.first()
        serializer = CreateQuestionSerializer(question)

        self.assertEqual(response.data, serializer.data)

    @auth
    def test_change_question_view(self):
        '''изменение вопроса'''
        survey = Survey.objects.create(
            is_active=True,
            start=timezone.now(),
            end=timezone.now()
        )
        Question.objects.create(
            text='text',
            type=1,
            survey=survey
        )

        url = reverse('question:change', args=[1])
        response = self.client.patch(url, data={'text': 'text1'}, format='json')
        question = Question.objects.first()

        self.assertEqual(response.data['text'], question.text)

    @auth
    def test_delete_question_view(self):
        '''удаление вопроса'''
        survey = Survey.objects.create(
            is_active=True,
            start=timezone.now(),
            end=timezone.now()
        )
        Question.objects.create(
            text='text',
            type=1,
            survey=survey
        )
        question = Question.objects.create(
            text='text',
            type=1,
            survey=survey
        )

        url = reverse('question:delete', args=[1])
        self.client.delete(url, format='json')
        questions = Question.objects.all()

        self.assertIn(question, questions)

    @auth
    def test_except_question_does_not_exist(self):
        '''исключение: вопроса не существует'''
        cl = self.client
        delete, patch = cl.delete, cl.patch
        for action in (('change', patch), ('delete', delete)):
            name_action, method = action
            url = reverse('question:' + name_action, args=[1])
            response = method(url, data={}, forma='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
