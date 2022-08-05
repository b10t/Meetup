import logging
from enum import Enum, auto

from django.conf import settings
from django.core.management.base import BaseCommand
from event.models import Participant
from telegram import (ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      ParseMode, ReplyKeyboardRemove, Update, chat)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils import helpers

import tgbot.management.commands._ask_question as ask_question

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class States(Enum):
    SHOW_MEETUPS = auto()
    ASK_QUESTION = auto()


STOPPING, SHOWING = map(chr, range(8, 10))


def start_handler(update: Update, context: CallbackContext):
    inl_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    '📋 Программа',
                    callback_data='SHOW_MEETUPS'
                )
            ],
            [
                InlineKeyboardButton(
                    '🗣 Задать вопрос спикеру',
                    callback_data='ASK_QUESTION'
                )
            ]
        ]
    )

    telegram_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name if update.message.chat.last_name else ''

    participant, _ = Participant.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'fio': f'{last_name} {first_name}'.strip()
        }
    )

    update.message.reply_text(
        f'Здравствуйте, {participant.fio}\.\n'
        'Это официальный бот по поддержке участников\. 🤖 \n',
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=inl_keyboard
    )
    # return 'callback_select_main_menu'
    return States.ASK_QUESTION


def callback_select_main_menu(update: Update, context: CallbackContext):
    """."""
    bot = update.effective_message.bot
    query = update.callback_query

    if query.data == 'SHOW_MEETUPS':
        return States.SHOW_MEETUPS
    elif query.data == 'ASK_QUESTION':
        return States.ASK_QUESTION
    else:
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and end the conversation."""
    update.message.reply_text(
        'Всего доброго!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


class Command(BaseCommand):
    help = 'Telegram Bot Meetup'

    def handle(self, *args, **options):
        TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

        print('Start Telegram Bot')
        print(f'{TELEGRAM_TOKEN=}')

        updater = Updater(token=TELEGRAM_TOKEN)

        dispatcher = updater.dispatcher

        conversation = ConversationHandler(
            name='main_conv',
            entry_points=[CommandHandler(
                'start', start_handler)],  # type: ignore
            states={
                STOPPING: [CommandHandler('start', start_handler)],
                'callback_select_main_menu': [
                    CallbackQueryHandler(
                        callback_select_main_menu
                    )
                ],
                States.ASK_QUESTION: [
                    ask_question.question_conv
                ],

                # 'join_the_game': [
                #     MessageHandler(
                #         Filters.text & ~Filters.command,
                #         join_the_game
                #     )
                # ],
                # 'get_game_name': [
                #     MessageHandler(
                #         Filters.text & ~Filters.command,
                #         get_game_name
                #     )
                # ],
                # 'callback_cost_gift': [
                #     CallbackQueryHandler(
                #         callback_cost_gift
                #     )
                # ],
                # 'callback_registration_period': [
                #     CallbackQueryHandler(
                #         callback_registration_period
                #     )
                # ],
                # 'get_dispatch_date': [
                #     MessageHandler(
                #         Filters.text & ~Filters.command,
                #         get_dispatch_date
                #     )
                # ],
            },  # type: ignore
            fallbacks=[
                CommandHandler('cancel', cancel)],  # type: ignore
        )

        dispatcher.add_handler(conversation)

        updater.start_polling()
        updater.idle()
