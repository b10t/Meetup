from django.contrib import admin
from event.models import Participant, Meetup, MeetupDetail
from django.utils.html import format_html


class MeetupDetailInline(admin.StackedInline):
    model = MeetupDetail
    extra = 0


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    inlines = [MeetupDetailInline]
    save_on_top = True


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fields = ('preview_image', 'fio', 'telegram_id', 'email', 'phone', 'company', 'position', 'image')
    readonly_fields = ['preview_image']
    save_on_top = True

    def preview_image(self, obj):
        return format_html('<img src="{}" height={} />', obj.image.url, 200)
