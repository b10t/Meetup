from django.contrib import admin
from event.models import Participant, Meetup, Event, EventParticipant, Question, Notification
from django.utils.html import format_html


EXTRA = 0
SAVE_ON_TOP = True


class EventParticipantInLine(admin.TabularInline):
    fields = ('event', ('participant', 'status'), )
    model = EventParticipant
    extra = EXTRA


class EventlInline(admin.StackedInline):
    fields = (('pos_num', 'name'), 'description', 'location', ('moment_from', 'moment_to'))
    model = Event
    extra = EXTRA


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'location', ('moment_from', 'moment_to'))
    inlines = [EventlInline]
    save_on_top = SAVE_ON_TOP


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fields = (('preview_image', 'image'), ('fio', 'telegram_id'), ('company', 'position'), ('email', 'phone'))
    list_display = ('telegram_id', 'fio', 'company', 'position', )
    readonly_fields = ['preview_image']
    save_on_top = SAVE_ON_TOP

    def preview_image(self, obj):
        return format_html('<img src="{}" height={} />', obj.image.url, 200)

    preview_image.short_description = 'Аватарка'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ('meetup', ('pos_num', 'type', 'name'), 'location', 'description', ('moment_from', 'moment_to'))
    inlines = [EventParticipantInLine]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'asker', 'short_question', )
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
