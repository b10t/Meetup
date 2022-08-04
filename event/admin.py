from django.contrib import admin
from event.models import Participant, Meetup, Event, EventParticipant
from django.utils.html import format_html


class EventlInline(admin.StackedInline):
    fields = (('name', 'type'), 'description', 'location', ('moment_from', 'moment_to'))
    model = Event
    extra = 0


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'location', ('moment_from', 'moment_to'))
    inlines = [EventlInline]
    save_on_top = True


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fields = ('preview_image', 'fio', 'telegram_id', 'email', 'phone', 'company', 'position', 'image')
    readonly_fields = ['preview_image']
    save_on_top = True

    def preview_image(self, obj):
        return format_html('<img src="{}" height={} />', obj.image.url, 200)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    pass
