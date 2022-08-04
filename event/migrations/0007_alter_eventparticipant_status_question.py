# Generated by Django 4.0.6 on 2022-08-04 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='status',
            field=models.CharField(choices=[('listener', 'слушатель'), ('speaker', 'докладчик')], db_index=True, max_length=10, verbose_name='Статус участника'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Текст вопроса')),
                ('asker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='askers', to='event.eventparticipant', verbose_name='Кто задал вопрос')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speakers', to='event.eventparticipant', verbose_name='Докладчики на событии')),
            ],
            options={
                'verbose_name': 'Вопрос докладчику',
                'verbose_name_plural': 'Вопросы докладчику',
            },
        ),
    ]
