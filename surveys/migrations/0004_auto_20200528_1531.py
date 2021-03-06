# Generated by Django 2.2.10 on 2020-05-28 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20200528_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='create_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата старта опроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.CharField(max_length=255, verbose_name='Описание опроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='end_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания опроса'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Имя опроса'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст вопроса')),
                ('type', models.IntegerField(choices=[(1, 'Текстовый ответ'), (2, 'Единственный ответ'), (3, 'Множественный ответ')], default=1, verbose_name='Тип вопроса')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey', verbose_name='Id опроса')),
            ],
        ),
    ]
