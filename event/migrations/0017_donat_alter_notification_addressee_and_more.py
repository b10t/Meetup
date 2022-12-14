# Generated by Django 4.0.6 on 2022-08-07 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0016_rename_asked_question_answered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressee', models.BigIntegerField(db_index=True, verbose_name='Телеграм ID донатируемого')),
                ('summa', models.IntegerField(verbose_name='Сумма доната')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время доната')),
                ('delivered', models.BooleanField(verbose_name='Доставлено')),
            ],
            options={
                'verbose_name': 'Донат',
                'verbose_name_plural': 'Донаты',
            },
        ),
        migrations.AlterField(
            model_name='notification',
            name='addressee',
            field=models.BigIntegerField(db_index=True, verbose_name='Телеграм ID адресата'),
        ),
        migrations.AlterField(
            model_name='question',
            name='asker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_of_askers', to='event.eventparticipant', verbose_name='Кто задал вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='speaker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_to_speaker', to='event.eventparticipant', verbose_name='Докладчики на событии'),
        ),
    ]
