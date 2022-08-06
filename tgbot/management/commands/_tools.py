from event.models import Meetup, Event


def get_meetups():
    meetups = Meetup.objects.all()
    return [meetup for meetup in meetups]


def get_event(meetup_id):
    events = Event.objects.filter(meetup_id=meetup_id)
    return [event for event in events]
