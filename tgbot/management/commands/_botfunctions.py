import re

import django
from django.utils import timezone

from event.models import Participant, Event, EventParticipant, Meetup, Question, Donat


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

    return {
        'meetups': meetups
    }


def get_meetup_at_now():
    """
    Возвращает список митапов на сейчас
    """
    moment = timezone.now()
    events = Event.objects.filter(moment_to__gte=moment, moment_from__lte=moment)

    # events.list ?...

    if not events:
        return []

    meetup_ids = []
    for event in events:
        meetup_ids.append(event.meetup.id)
    meetup_ids = list(set(meetup_ids))

    meetups = Meetup.objects.filter(id__in=meetup_ids)
    result = []
    for meetup in meetups:
        result.append({'meetup': meetup})
    return result


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


def get_acquaintance_descr():
    """
    Возвращает описание процесса знакомства с участниками
    """
    return """Описание процесса знакомства с участниками"""


def get_speaker_questions(speaker, event=None, answered=None):
    """
    Возвращает список заданных speaker-у вопросов.
    speaker - EventParticipant или int
    event - Event
    answered - bool: True - отвеченных, False - неотвеченных, None - всех
    """
    if isinstance(speaker, EventParticipant):
        if answered is None:
            questions = speaker.questions_to_speaker.all()
        else:
            questions = speaker.questions_to_speaker.all().filter(answered=answered)
    elif isinstance(speaker, int) and isinstance(event, Event):
        participant = Participant.objects.get(telegram_id=speaker)
        event_participant = EventParticipant.objects.get(event=event, participant=participant)
        if answered is None:
            questions = event_participant.questions_to_speaker.all()
        else:
            questions = event_participant.questions_to_speaker.all().filter(answered=answered)

    result = []
    for question in questions:
        result.append({
            'speaker': question.speaker.participant,
            'speaker_fio': question.speaker.participant.fio,
            'speaker_tg_id': question.speaker.participant.telegram_id,
            'asker': question.asker.participant,
            'asker_fio': question.asker.participant.fio,
            'asker_tg_id': question.asker.participant.telegram_id,
            'question': question.question,
            'answered': question.answered,
            'moment': format_datetime(question.moment)
        })
    return result


def get_telegram_id(participant):
    """
    Возвращает telegram_id участника
    participant: int, Participant, EventParticipant
    """
    if isinstance(participant, int):
        return participant
    elif isinstance(participant, Participant):
        return participant.telegram_id
    elif isinstance(participant, EventParticipant):
        return participant.participant.telegram_id
    else:
        raise TypeError(f'participant может быть int, Participant или EventParticipant, но не {type(participant)}')


def get_donates(participant=None):
    """
    Возвращает весь список донатов или для конкретного участника
    participant: int, Participant, EventParticipant
    """
    if participant is None:
        donates = Donat.objects.all()
    else:
        donates = Donat.objects.all().filter(addressee=get_telegram_id(participant))

    result = []
    for donate in donates:
        result.append({
            'addressee': donate.addressee,
            'summa': donate.summa,
            'moment': format_datetime(donate.created_at)
        })
    return result