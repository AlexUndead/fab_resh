from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator


class Survey(models.Model):
    """Модель опроса"""
    name = models.CharField(max_length=255, verbose_name='Имя опроса')
    create_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата старта опроса. Формат: YYYY-MM-DD HH:MM:SS')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания опроса. Формат: YYYY-MM-DD HH:MM:SS')
    description = models.CharField(max_length=255, verbose_name='Описание опроса')


class Question(models.Model):
    """Модель вопросов"""
    QUESTION_TYPES = (
        (1, 'Текстовый ответ'),
        (2, 'Единственный ответ'),
        (3, 'Множественный ответ'),
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Id опроса')
    text = models.CharField(max_length=255, verbose_name='Текст вопроса')
    type = models.IntegerField(choices=QUESTION_TYPES, default=1, verbose_name='Тип вопроса')


class Answer(models.Model):
    """Модель ответов на вопросы"""
    ANSWER_TYPES = (
        (1, 'Неправильный ответ'),
        (2, 'Правильный ответ'),
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Id вопроса')
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    type = models.IntegerField(choices=ANSWER_TYPES, default=0, verbose_name='Тип ответа')


class Result(models.Model):
    """Модель прохождения опросов"""
    slug = models.SlugField(max_length=20, unique=True)
    user_id = models.IntegerField(blank=True, default=0)
    result = models.TextField()


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_save, sender=Result)



