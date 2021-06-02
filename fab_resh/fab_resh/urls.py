from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='Тестовое задание Фабрики решений',
        default_version='v1',
        description='API для системы опросов'
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('survey/', view=include('survey.urls.survey_urls', namespace='survey')),
    path('question/', view=include('survey.urls.question_urls', namespace='question')),
]

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
