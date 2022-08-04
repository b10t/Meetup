# Generated by Django 4.0.6 on 2022-08-04 13:28

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_alter_eventparticipant_status_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressee', models.BigIntegerField(db_index=True, unique=True, verbose_name='Телеграм ID')),
                ('message', tinymce.models.HTMLField(verbose_name='Текст сообщения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания оповещения')),
                ('delivered', models.BooleanField(verbose_name='Доставлено')),
            ],
            options={
                'verbose_name': 'Оповещение',
                'verbose_name_plural': 'Оповещения',
            },
        ),
    ]
