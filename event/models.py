from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator


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
    description = HTMLField(verbose_name='Описание', blank=True)
    location = HTMLField(verbose_name='Место проведения', blank=True)
    moment_from = models.DateTimeField(verbose_name='Дата и время начала', blank=True)
    moment_to = models.DateTimeField(verbose_name='Дата и время окончания', blank=True)

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
    name = models.CharField(max_length=255, verbose_name='Название события')
    description = HTMLField(verbose_name='Описание события', blank=True)
    location = models.TextField(verbose_name='Место прохождения', blank=True)
    type = models.CharField(max_length=10, verbose_name='Тип события', choices=MEETUP_TYPE, default='primary')
    moment_from = models.DateTimeField(verbose_name='Время начала', blank=True)
    moment_to = models.DateTimeField(verbose_name='Время окончания', blank=True)
    pos_num = models.IntegerField(verbose_name='Порядковый №', default=1, validators=[MinValueValidator(1)])

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
    speaker = models.ForeignKey(EventParticipant, related_name='questions_to_speaker', verbose_name='Докладчики на событии',
                                on_delete=models.CASCADE)
    asker = models.ForeignKey(EventParticipant, related_name='questions_of_askers', verbose_name='Кто задал вопрос',
                              on_delete=models.CASCADE)
    question = models.TextField(verbose_name='Текст вопроса')
    moment = models.DateTimeField(verbose_name='Дата и время создания вопроса', auto_now_add=True)
    answered = models.BooleanField(verbose_name='Вопрос отвечен', default=False)

    class Meta:
        verbose_name = 'Вопрос докладчику'
        verbose_name_plural = 'Вопросы докладчику'

    def short_question(self):
        return self.question[:100]
    short_question.short_description = 'Начало текста вопроса'

    def __str__(self):
        speaker = self.speaker
        return f'{speaker.event}: {speaker.participant} -> {self.asker.participant} ({self.answered})'


class Notification(models.Model):
    addressee = models.BigIntegerField(verbose_name='Телеграм ID адресата', db_index=True)
    message = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(verbose_name='Дата и время создания оповещения', auto_now_add=True)
    delivered = models.BooleanField(verbose_name='Доставлено')

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'

    def __str__(self):
        return f'{self.addressee}, {self.message[:100]}...'


class Donat(models.Model):
    addressee = models.BigIntegerField(verbose_name='Телеграм ID донатируемого', db_index=True)
    summa = models.IntegerField(verbose_name='Сумма доната')
    created_at = models.DateTimeField(verbose_name='Дата и время доната', auto_now_add=True)
    delivered = models.BooleanField(verbose_name='Доставлено')

    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'

    def __str__(self):
        return f'{self.addressee}, {self.summa}'


