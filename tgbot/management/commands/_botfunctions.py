from event.models import Meetup, Event, EventParticipant
import re
from datetime import datetime, timezone
import django
from datetime import timedelta


def html2txt(html):
    return re.sub(r'<(.*?)>', '', html)


def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_meetups(today=True):
    """
    Возвращает список мероприятий
    moment == None
        возвращает полный список мероприятий, days не используется
    else
        возвращает список мероприятий от moment на следующие days дней
    """
    if today:
        moment = django.utils.timezone.now()  # - timedelta(days=1)
        meetups = Meetup.objects.all().filter(moment_to__gte=moment, moment_from__lte=moment)
    else:
        meetups = Meetup.objects.all()

    return meetups


def get_meetup_events(meetup_id):
    """
    Возвращает список событий указанного мероприятия.
    Текущее событие имеет признак current=True
    """

    result = []
    for event in Event.objects.filter(meetup=meetup_id):
        result.append(
            {
                'name': event.name,
                'description': html2txt(event.description),
                'location': html2txt(event.location),
                'moment_from': format_datetime(event.moment_from),
                'moment_to': format_datetime(event.moment_to),
                'current': False  # TODO
            }
        )
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
    for event in EventParticipant.objects.filter(event=event):
        result.append({
            'tg_id': event.participant.telegram_id,
            'fio': event.participant.fio
        })
    return result

