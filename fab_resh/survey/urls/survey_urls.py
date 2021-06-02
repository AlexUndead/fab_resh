from django.urls import path, include
from ..views import survey_views, question_views

app_name = 'survey'
urlpatterns = [
    path(
        'create/',
        survey_views.CreateSurveyView.as_view(),
        name='create'
    ),
    path(
        'change/<id>/',
        survey_views.ChangeSurveyView.as_view(),
        name='change'
    ),
    path(
        'delete/<id>/',
        survey_views.DeleteSurveyView.as_view(),
        name='delete'
    ),
    path(
        'get/',
        survey_views.GetActiveSurveysView.as_view(),
        name='get'
    ),
    path(
        'get/<id>/',
        survey_views.GetSurveyView.as_view(),
        name='get_by_id'
    ),
    path(
        'user/<id>/',
        survey_views.GetUserResultView.as_view(),
        name='get_user_result'
    ),
    path(
        'run/<survey_id>/user/<user_id>/',
        survey_views.RunSurveyView.as_view(),
        name='run'
    ),
]
