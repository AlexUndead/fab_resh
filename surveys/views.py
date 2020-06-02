from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from rest_framework import generics, permissions
from .models import Survey, Question, Answer, Result
from .forms import SurveyForm, QuestionForm, AnswerForm
from .serializers import SurveyResultSerialize
from .validator import SurveyValidator
import json


def create_date_redirect(func):
    """декоратор редиректящий если у опроса есть дата старта"""
    def wrapper(self, request, survey_id, *args, **kwargs):
        if get_object_or_404(Survey, id=survey_id).create_at:
            return redirect('survey_error')

        return func(self, request, survey_id, *args, **kwargs)

    return wrapper


class IndexView(View):
    """Индексная страница"""

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})


class SurveysView(View):
    """Страница просмотра всех опросов"""

    def get(self, request, *args, **kwargs):
        return render(request, 'surveys_view.html', {'surveys': Survey.objects.all()})
        

class SurveyCreate(View):
    """Страница создания опроса"""
    def get(self, request, *args, **kwargs):
        form = SurveyForm()
        return render(request, 'survey_create.html', {'form': form})

    @create_date_redirect
    def post(self, request, *args, **kwargs):
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save()
            return redirect('survey_view', survey_id=survey.id)
        else:
            return render(request, 'survey_create.html', {'form': form})


class SurveyError(View):
    """Страница ошибки при изменении опроса с заданной датой начало"""
    def get(self, request):
        return render(request, 'survey_error.html', {})


class SurveyView(View):
    """Страница просмотра и редактирования опроса"""
    def get(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        data = {
            'name': survey.name,
            'create_at': survey.create_at,
            'end_at': survey.end_at,
            'description': survey.description
        }
        form = SurveyForm(data)
        return render(request, 'survey_view.html', {'form': form, 'survey': survey})

    @create_date_redirect
    def post(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        form = SurveyForm(request.POST, instance=survey)

        if form.is_valid():
            form.save()
            return redirect('survey_view', survey_id=survey_id)
        else:
            return render(request, 'survey_view.html', {'form': form, 'survey': survey})


class SurveyDelete(View):
    """Детальная удаления опроса"""
    def get(self, request, survey_id, *args, **kwargs):
        return redirect('survey_view', survey_id=survey_id)

    @create_date_redirect
    def post(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        survey.delete()

        return redirect('surveys_view')


class QuestionCreate(View):
    """Страница создания вопроса"""
    def get(self, request, survey_id, *args, **kwargs):
        question_form = QuestionForm()

        return render(request, 'question_create.html', {'question_form': question_form})

    @create_date_redirect
    def post(self, request, survey_id, *args, **kwargs):
        data = {
            'survey': survey_id,
            'text': request.POST['text'],
            'type': request.POST['type'],
        }
        question_form = QuestionForm(data)

        if question_form.is_valid():
            question_form.save()
            return redirect('survey_view', survey_id=survey_id)
        else:
            return render(request, 'question_create.html', {'question_form': question_form})


class QuestionView(View):
    """Страница просмотра и редактирования вопроса"""
    def get(self, request, survey_id, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        data = {
            'text': question.text,
            'type': question.type,
            'survey': question.survey,
        }
        question_form = QuestionForm(data)

        return render(request, 'question_view.html', {'question_form': question_form, 'question': question})

    @create_date_redirect
    def post(self, request, survey_id, question_id, *args, **kwargs):
        data = {
            'text': request.POST['text'],
            'type': request.POST['type'],
            'survey': survey_id,
        }
        question_form = QuestionForm(data, instance=Question.objects.get(id=question_id))

        if question_form.is_valid():
            question_form.save()
            return redirect('question_view', survey_id=survey_id, question_id=question_id)
        else:
            question = get_object_or_404(Question, id=question_id)
            return render(request, 'question_view.html', {'question_form': question_form, 'question': question})


class QuestionDelete(View):
    """Страница удаления вопроса"""
    def get(self, request, survey_id, question_id, *args, **kwargs):
        return redirect('survey_view', survey_id=survey_id)

    @create_date_redirect
    def post(self, request, survey_id, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        question.delete()

        return redirect('survey_view', survey_id=survey_id)


class AnswerCreate(View):
    """Страница создания ответа"""
    def get(self, request, survey_id, question_id, *args, **kwargs):
        answer_form = AnswerForm()
        return render(request, 'answer_create.html', {'answer_form': answer_form})

    @create_date_redirect
    def post(self, request, survey_id, question_id, *args, **kwargs):
        data = {
            'text': request.POST['text'],
            'type': request.POST['type'],
            'question': question_id
        }
        answer_form = AnswerForm(data)

        if answer_form.is_valid():
            answer_form.save()
            return redirect('question_view', survey_id=survey_id, question_id=question_id)
        else:
            return render(request, 'answer_create.html', {'answer_form': answer_form})


class AnswerView(View):
    """Страница просмотра и редактирования ответа"""
    def get(self, request, survey_id, question_id, answer_id, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_id)
        data = {
            'text': answer.text,
            'type': answer.type,
            'question': question_id
        }
        answer_form = AnswerForm(data)
        return render(request, 'answer_view.html', {'answer_form': answer_form, 'answer':answer})

    @create_date_redirect
    def post(self, request, survey_id, question_id, answer_id, *args, **kwargs):
        data = {
            'text': request.POST['text'],
            'type': request.POST['type'],
            'question': question_id
        }
        answer_form = AnswerForm(data, instance=Question.objects.get(id=question_id))

        if answer_form.is_valid():
            answer_form.save()
            return redirect('question_view', question_id=question_id, answer_id=answer_id)
        else:
            answer = get_object_or_404(Answer, id=answer_id)
            return render(request, 'answer_view.html', {'answer_form': answer_form, 'answer': answer})


class AnswerDelete(View):
    """Страница удаления ответа"""
    def get(self, request, survey_id, question_id, answer_id, *args, **kwargs):
        return redirect('question_view', survey_id=survey_id, question_id=question_id)

    @create_date_redirect
    def post(self, request, survey_id, question_id, answer_id, *args, **kwargs):
        answer = get_object_or_404(Answer, id=answer_id)
        answer.delete()

        return redirect('question_view', survey_id=survey_id, question_id=question_id)


class CustomerSurveysView(View):
    """Страница списка всех опросов"""
    def get(self, request, *args, **kwargs):
        surveys = Survey.objects.all()
        return render(request, 'customer_surveys_view.html', {'surveys': surveys})


class CustomerSurveyRun(View):
    """Страница прохождния опроса"""
    def get(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        return render(request, 'customer_survey_run.html', {'survey': survey})


class CustomerSurveyResultSave(generics.CreateAPIView):
    """Страница сохранения результата прохождения опроса"""
    def get_serializer(self, *args, **kwargs):
        """
        Добавления user_id если пользователь зарегистрирован и
        перконвертирование результата в строковый фармат
        """
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        draft_request_data = self.request.data.copy()

        if self.request.user.id:
            draft_request_data['user_id'] = self.request.user.id

        draft_request_data['result'] = json.dumps(self.request.data.get('result'), ensure_ascii=False)
        kwargs['data'] = draft_request_data

        return serializer_class(*args, **kwargs)

    serializer_class = SurveyResultSerialize
    queryset = Result.objects.all()
    permission_classes = (permissions.AllowAny, )


class CustomerSurveyResultView(View):
    """Страница просмотра результата опроса"""
    def get(self, request, slug, *args, **kwargs):
        customer_result_obj = get_object_or_404(Result, slug=slug)
        customer_result_decode = json.loads(customer_result_obj.result)
        validator_survey = SurveyValidator(customer_result_decode)
        valid_survey_result = validator_survey.validation()

        return render(request, 'customer_survey_result_view.html', {'valid_survey_result': valid_survey_result})
