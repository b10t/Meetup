from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Telegram Bot Meetup'

    def handle(self, *args, **options):
        TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

        print('Start Telegram Bot')
        print(TELEGRAM_TOKEN)
