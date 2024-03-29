# Generated by Django 2.2.10 on 2021-05-30 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='активность')),
                ('name', models.CharField(max_length=50, verbose_name='имя')),
                ('discription', models.CharField(max_length=250, verbose_name='описание')),
                ('start', models.DateTimeField(verbose_name='время начала')),
                ('end', models.DateTimeField(verbose_name='время конца')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='SurveySession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey', verbose_name='опрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.User', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'сессия опроса',
                'verbose_name_plural': 'сессии ответов',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст')),
                ('type', models.SmallIntegerField(choices=[(0, 'ответ текстом'), (1, 'ответ с выбором одного варианта'), (2, 'ответ с выбором нескольких вариантов')], default=0, verbose_name='тип')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey', verbose_name='опрос')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='текст')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Question', verbose_name='вопрос')),
                ('survey_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.SurveySession', verbose_name='сессия опроса')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
    ]
