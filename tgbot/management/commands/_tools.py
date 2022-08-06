from enum import Enum, auto

from event.models import Meetup


class States(Enum):
    """Состояния бота."""
    SHOW_MEETUPS = 'SHOW_MEETUPS'
    BACK_TO_MAIN_MENU = 'BACK_TO_MAIN_MENU'
    START_OVER = 'START_OVER'
    SELECT_MEETUP = 'SELECT_MEETUP'


def get_meetups():
    meetups = Meetup.objects.all()
    return [meetup.name for meetup in meetups]
