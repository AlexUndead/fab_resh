from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/surveys/view/', views.SurveysView.as_view(), name='surveys_view'),
    path('admin/survey/create/', views.SurveyCreate.as_view(), name='survey_create'),
    path('admin/survey/view/<int:survey_id>/', views.SurveyView.as_view(), name='survey_view'),
    path('admin/survey/delete/<int:survey_id>/', views.SurveyDelete.as_view(), name='survey_delete'),
    path(
        'admin/survey/<int:survey_id>/question/create/',
        views.QuestionCreate.as_view(),
        name='question_create'
    ),
    path(
        'admin/survey/<int:survey_id>/question/view/<int:question_id>/',
        views.QuestionView.as_view(),
        name='question_view'
    ),
    path(
        'admin/survey/<int:survey_id>/question/delete/<int:question_id>/',
        views.QuestionDelete.as_view(),
        name='question_delete'
    ),
    path(
        'admin/survey/<int:survey_id>/question/<int:question_id>/create/',
        views.AnswerCreate.as_view(),
        name='answer_create'
    ),
    path(
        'admin/survey/<int:survey_id>/question/<int:question_id>/view/<int:answer_id>/',
        views.AnswerView.as_view(),
        name='answer_view'
    ),
    path(
        'admin/survey/<int:survey_id>/question/<int:question_id>/delete/<int:answer_id>/',
        views.AnswerDelete.as_view(),
        name='answer_delete'
    ),
    path(
        'surveys/view/',
        views.CustomerSurveysView.as_view(),
        name='customer_surveys_view'
    ),
    path(
        'surveys/run/<int:survey_id>/',
        views.CustomerSurveyRun.as_view(),
        name='customer_survey_run'
    ),
    path(
        'surveys/result/save/',
        views.CustomerSurveySave.as_view(),
        name='customer_survey_save'
    ),

]
