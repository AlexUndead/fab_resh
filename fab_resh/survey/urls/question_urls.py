from django.urls import path, include
from ..views import survey_views, question_views

app_name = 'question'
urlpatterns = [
    path(
        'create/',
        question_views.CreateQuestionView.as_view(),
        name='create'
    ),
    path(
        'change/<id>/',
        question_views.ChangeQuestionView.as_view(),
        name='change'
    ),
    path(
        'delete/<id>/',
        question_views.DeleteQuestionView.as_view(),
        name='delete'
    ),
]
