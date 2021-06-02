from django.db import models

FREE = 0
ONE_ANSWER = 1
LOTS_ANSWERS = 2
TYPE_CHOICES = (
    (FREE, 'ответ текстом'),
    (ONE_ANSWER, 'ответ с выбором одного варианта'),
    (LOTS_ANSWERS, 'ответ с выбором нескольких вариантов')
)


class User(models.Model):
    '''Пользователь'''

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return str(f'Пользователь: {self.id}')


class Survey(models.Model):
    '''Опрос'''
    is_active = models.BooleanField(verbose_name='активность', default=True)
    name = models.CharField(verbose_name='имя', max_length=50)
    description = models.CharField(verbose_name='описание', max_length=250)
    start = models.DateTimeField(verbose_name='время начала')
    end = models.DateTimeField(verbose_name='время конца')

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return str(f'Опрос: {self.id}')


class Question(models.Model):
    '''Вопрос'''
    text = models.TextField(verbose_name='текст')
    type = models.SmallIntegerField(
        verbose_name='тип',
        choices=TYPE_CHOICES,
        default=FREE
    )
    survey = models.ForeignKey(
        to=Survey,
        verbose_name='опрос',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return str(f'Вопрос: {self.id}')


class SurveySession(models.Model):
    '''сессия опроса'''
    user = models.ForeignKey(
        to=User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        to=Survey,
        verbose_name='опрос',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'сессия опроса'
        verbose_name_plural = 'сессии опросов'

    def __str__(self):
        return str(f'Сессия опроса: {self.id}')


class Answer(models.Model):
    '''ответ'''
    question = models.ForeignKey(
        to=Question,
        verbose_name='вопрос',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='текст')
    survey_session = models.ForeignKey(
        to=SurveySession,
        verbose_name='сессия опроса',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return str(f'Ответ: {self.id}')
