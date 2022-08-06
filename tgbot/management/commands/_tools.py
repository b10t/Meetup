from event.models import Meetup, Event


def get_event(meetup_id):
    events = Event.objects.filter(meetup_id=meetup_id)
    return [event for event in events]


def get_message(event_id):
    event = Event.objects.get(id=event_id)
    message = event.description
    return message


def get_meetups():
    meetups = Meetup.objects.all()
    return [meetup for meetup in meetups]
