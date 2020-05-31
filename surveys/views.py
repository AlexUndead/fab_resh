from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from rest_framework import generics, permissions
from .models import Survey, Question, Answer, Result
from .forms import SurveyForm, QuestionForm, AnswerForm
from .serializers import SurveyResultSerialize


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

    def post(self, request, *args, **kwargs):
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save()
            return redirect('survey_view', survey_id=survey.id)


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

    def post(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        form = SurveyForm(request.POST, instance=survey)

        if form.is_valid():
            form.save()

        return redirect('survey_view', survey_id=survey_id)


class SurveyDelete(View):
    """Детальная удаления опроса"""
    def get(self, request, survey_id, *args, **kwargs):
        return redirect('survey_view', survey_id=survey_id)

    def post(self, request, survey_id, *args, **kwargs):
        survey = get_object_or_404(Survey, id=survey_id)
        survey.delete()

        return redirect('surveys_view')


class QuestionCreate(View):
    """Страница создания вопроса"""
    def get(self, request, survey_id, *args, **kwargs):
        question_form = QuestionForm()

        return render(request, 'question_create.html', {'question_form': question_form})

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


class QuestionDelete(View):
    """Страница удаления вопроса"""
    def get(self, request, survey_id, question_id, *args, **kwargs):
        return redirect('survey_view', survey_id=survey_id)

    def post(self, request, survey_id, question_id, *args, **kwargs):
        question = get_object_or_404(Question, id=question_id)
        question.delete()

        return redirect('survey_view', survey_id=survey_id)


class AnswerCreate(View):
    """Страница создания ответа"""
    def get(self, request, survey_id, question_id, *args, **kwargs):
        answer_form = AnswerForm()
        return render(request, 'answer_create.html', {'answer_form': answer_form})

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


class AnswerDelete(View):
    """Страница удаления ответа"""
    def get(self, request, survey_id, question_id, answer_id, *args, **kwargs):
        return redirect('question_view', survey_id=survey_id, question_id=question_id)

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


class CustomerSurveySave(generics.CreateAPIView):
    """Страница сохранения результата прохождения опроса"""
    #def post(self, request, *args, **kwargs):
        # data = {
        #     'user': request.user.id if request.user.id else 0,
        #     'result': request.POST['result'],
        # }
        # super().post(request, *args, **kwargs)

    serializer_class = SurveyResultSerialize
    queryset = Result.objects.all()
    permission_classes = (permissions.AllowAny, )
