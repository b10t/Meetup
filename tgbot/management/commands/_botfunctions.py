import re

import django
from django.utils import timezone

from event.models import Event, EventParticipant, Meetup, Question


def html2txt(html):
    return re.sub(r'<(.*?)>', '', html)


def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_meetups(today=True):
    """
    Возвращает список мероприятий
    moment == None
        возвращает полный список мероприятий
    else
        возвращает список активных на сегодня мероприятий
    """
    if today:
        moment = django.utils.timezone.now()
        meetups = Meetup.objects.all().filter(moment_to__gte=moment, moment_from__lte=moment)
    else:
        meetups = Meetup.objects.all()

    return meetups


def get_meetup_events(meetup, current=False):
    """
    Возвращает список событий указанного мероприятия.
    Текущее событие имеет признак current=True
    """

    moment = timezone.now()
    if current:
        events = Event.objects.filter(meetup=meetup, moment_to__gte=moment, moment_from__lte=moment)
    else:
        events = Event.objects.filter(meetup=meetup)

    result = []
    for event in events:
        result.append({
            'event': event,
            'current': event.moment_to >= moment >= event.moment_from
        })
    return result


def get_meetup_participants(meetup):
    """
    Возвращает список участников мероприятия
    """
    result = []
    for event in Event.objects.filter(meetup=meetup):
        for event_participant in event.participants.all():
            result.append({
                'tg_id': event_participant.participant.telegram_id,
                'fio': event_participant.participant.fio
            })
    return result


def get_event_participants(event):
    """
    Возвращает список участников события
    """
    result = []
    for event_participant in EventParticipant.objects.filter(event=event):
        result.append({
            'tg_id': event_participant.participant.telegram_id,
            'fio': event_participant.participant.fio,
            'status': event_participant.status
        })
    return result


def get_participant_descr(event, participant):
    """
    Возвращает данные участника: анкета, статус
    """
    event_participant = EventParticipant.objects.all().get(event=event, participant=participant)
    return {
        'fio': event_participant.participant.fio,
        'telegram_id': event_participant.participant.telegram_id,
        'email': event_participant.participant.email,
        'phone': event_participant.participant.phone,
        'company': event_participant.participant.company,
        'position': event_participant.participant.position,
        'image': event_participant.participant.image,
        'status': event_participant.status
    }


def get_bot_funcs_descr():
    """
    Возвращает общее описание бота
    """
    return """Общее описание бота"""


def save_question(speaker, asker, question):
    return Question.objects.create(speaker=speaker, asker=asker, question=question)
