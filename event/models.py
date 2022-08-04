from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField


LISTENER = 'listener'
SPEAKER = 'speaker'

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


class Event(models.Model):
    MEETUP_TYPE = (
        ('primary', 'Основное'),
        ('secondary', 'Вспомогательное'),
    )
    meetup = models.ForeignKey(Meetup, verbose_name='Мероприятие', related_name='events', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название события', blank=False)
    description = HTMLField(verbose_name='Описание события')
    location = models.TextField(verbose_name='Место прохождения', blank=False)
    type = models.CharField(max_length=10, verbose_name='Тип события', choices=MEETUP_TYPE, default='primary')
    moment_from = models.DateTimeField(verbose_name='Время начала')
    moment_to = models.DateTimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'Событие мероприятия'
        verbose_name_plural = 'События мероприятий'

    def __str__(self):
        return f'{self.meetup} - {self.name}'


class EventParticipantQuerySet(models.QuerySet):
    def get_speakers(self):
        return self.filter(status='speaker')


class EventParticipant(models.Model):
    PARTICIPANT_STATUS = (
        (LISTENER, 'слушатель'),
        (SPEAKER, 'докладчик')
    )
    event = models.ForeignKey(Event, verbose_name='Событие', on_delete=models.CASCADE,
                              related_name='participants')
    participant = models.ForeignKey(Participant, verbose_name='Участник события', on_delete=models.CASCADE,
                                    related_name='events')
    status = models.CharField(max_length=10, verbose_name='Статус участника', choices=PARTICIPANT_STATUS, db_index=True)

    objects = EventParticipantQuerySet.as_manager()

    class Meta:
        verbose_name = 'Участник события'
        verbose_name_plural = 'Участники событий'

    def __str__(self):
        return f'{self.event} - {self.participant} ({self.get_status_display()})'


class Question(models.Model):
    speaker = models.ForeignKey(EventParticipant, related_name='speakers', verbose_name='Докладчики на событии',
                                on_delete=models.CASCADE)
    asker = models.ForeignKey(EventParticipant, related_name='askers', verbose_name='Кто задал вопрос',
                              on_delete=models.CASCADE)
    question = models.TextField(verbose_name='Текст вопроса')

    class Meta:
        verbose_name = 'Вопрос докладчику'
        verbose_name_plural = 'Вопросы докладчику'

    def short_question(self):
        return self.question[:100]
    short_question.short_description = 'Начало текста вопроса'

    def __str__(self):
        speaker = self.speaker
        return f'{speaker.event}, {speaker.participant} - {self.asker.participant}'
