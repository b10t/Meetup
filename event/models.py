from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField


class Participant(models.Model):
    fio = models.CharField(max_length=255, verbose_name='ФИО', db_index=True)
    telegram_id = models.BigIntegerField(verbose_name='Телеграм ID', unique=True, db_index=True)
    email = models.EmailField(verbose_name='Эл. почта', max_length=100, blank=True, db_index=True)
    phone = PhoneNumberField(verbose_name='Контактный телефон', blank=True, db_index=True)
    company = models.CharField(verbose_name='Компания', max_length=255, blank=True, db_index=True)
    position = models.CharField(verbose_name='Должность', max_length=255, blank=True)
    image = models.ImageField(verbose_name='Аватарка', default='', blank=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.telegram_id}, {self.fio}'


class Meetup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование', db_index=True)
    description = HTMLField(verbose_name='Описание')
    location = HTMLField(verbose_name='Место проведения', blank=False)
    moment_from = models.DateTimeField(verbose_name='Дата и время начала')
    moment_to = models.DateTimeField(verbose_name='Дата и время окончания')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.name


class MeetupDetail(models.Model):
    MEETUP_TYPE = (
        ('primary', 'Основное'),
        ('secondary', 'Вспомогательное'),
    )
    meetup = models.ForeignKey(Meetup, verbose_name='Мероприятие', related_name='meetup', on_delete=models.CASCADE)
    event = models.CharField(max_length=255, verbose_name='Событие', blank=False)
    description = HTMLField(verbose_name='Описание события')
    type = models.CharField(max_length=10, verbose_name='Тип события', choices=MEETUP_TYPE, default='primary')
    moment_from = models.DateTimeField(verbose_name='Время начала')
    moment_to = models.DateTimeField(verbose_name='Время окончания')
    speakers = models.ManyToManyField(Participant, verbose_name='Докладчики', related_name='event_speakers',
                                      blank=True)

    class Meta:
        verbose_name = 'Детали мероприятия'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.event
