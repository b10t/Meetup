from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Telegram Bot Meetup'

    def handle(self, *args, **options):
        print('Start Telegram Bot')
