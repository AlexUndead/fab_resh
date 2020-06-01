from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from rest_framework import generics, permissions
from .models import Survey, Question, Answer, Result
from .forms import SurveyForm, QuestionForm, AnswerForm
from .serializers import SurveyResultSerialize
import json


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
        else:
            return render(request, 'survey_create.html', {'form': form})


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
        else:
            return render(request, 'survey_view.html', {'form': form, 'survey': survey})


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
        self.validation_survey(customer_result_decode)

        return render(request, 'customer_survey_result_view.html', {'valid_survey_result': customer_result_decode})

    def get_correct_answers(self, question_id):
        answer_correct_type_id = 2
        return Answer.objects.select_related('question').filter(
            type=answer_correct_type_id,
            question_id__in=question_id,
        )

    def open_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        customer_answer['question'] = Question.objects.get(id=customer_question_id).text
        customer_answer['correctly'] = None

    def single_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        correct_answer = correct_answers.filter(question_id=customer_question_id).first()
        correct_answer_text = correct_answer.text
        correctly = True if correct_answer_text == customer_answer['value'] else False
        customer_answer['question'] = correct_answer.question.text
        customer_answer['correctly'] = correctly
        customer_answer['correct_answer'] = correct_answer_text

    def multiple_answer_validator(self, correct_answers, customer_question_id, customer_answer):
        correct_answer = correct_answers.filter(question_id=customer_question_id)
        correct_answer_set = {answer.text for answer in correct_answer}
        correctly = True if correct_answer_set == set(customer_answer['value']) else False
        customer_answer['question'] = correct_answer.first().question.text
        customer_answer['correctly'] = correctly
        customer_answer['correct_answer'] = correct_answer_set

    def validation_survey(self, customer_result):
        correct_answers = self.get_correct_answers(customer_result.keys())
        for customer_answer in customer_result:
            if customer_result[customer_answer]['type'] == 1:
                self.open_answer_validator(correct_answers, customer_answer, customer_result[customer_answer])
            elif customer_result[customer_answer]['type'] == 2:
                self.single_answer_validator(correct_answers, customer_answer, customer_result[customer_answer])
            elif customer_result[customer_answer]['type'] == 3:
                self.multiple_answer_validator(correct_answers, customer_answer, customer_result[customer_answer])
