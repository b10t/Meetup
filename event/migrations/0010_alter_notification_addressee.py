# Generated by Django 4.0.6 on 2022-08-04 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_alter_notification_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='addressee',
            field=models.BigIntegerField(db_index=True, verbose_name='Телеграм ID'),
        ),
    ]
