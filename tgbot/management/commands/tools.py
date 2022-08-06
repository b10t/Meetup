from event.models import Meetup


def get_meetups():
    meetups = Meetup.objects.all()
    return [meetup.name for meetup in meetups]
