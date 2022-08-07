import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from event.models import Participant

from ._tools import (
    get_meetups,
    get_event,
    get_message,
)

from ._tools import (
    get_meetups,
    get_event,
)
from ._ask_question import (
    question_show_meetups,
    question_show_event,
)
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    ParseMode,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Updater
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


(
    HANDLE_MENU,
    HANDLE_MEETUP,
    HANDLE_EVENT,
    START_OVER
) = range(4)


def show_menu(update, context):
    text = 'Выберете действие:'

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    '📋 Программа',
                    callback_data='Программа'
                )
            ],
            [
                InlineKeyboardButton(
                    '🗣 Задать вопрос спикеру',
                    callback_data='Задать вопрос'
                )
            ]
        ]
    )

    if context.user_data.get(START_OVER):
        # Повторный заход
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=inl_keyboard
        )

    else:
        telegram_id = update.message.chat_id
        context.user_data['telegram_id'] = telegram_id

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
            parse_mode=ParseMode.MARKDOWN_V2
        )

        update.message.reply_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard
        )

    context.user_data[START_OVER] = True

    return HANDLE_MENU


def show_meetups(update, context):
    meetups = get_meetups()
    keyboard = list()
    for meetup in meetups:
        keyboard.append(
            [InlineKeyboardButton(meetup.name, callback_data=meetup.id)]
        )
    keyboard.append(
        [InlineKeyboardButton(
            'Главное меню',
            callback_data='Главное меню',
        )]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text='Выберите: ', reply_markup=reply_markup
    )
    return HANDLE_MEETUP


def show_event(update, context):
    meetup_id = update.callback_query.data
    events = get_event(meetup_id)
    keyboard = list()
    for event in events:
        keyboard.append(
            [InlineKeyboardButton(event.name, callback_data=event.id)]
        )
    keyboard.append(
        [InlineKeyboardButton('Назад', callback_data='Назад')]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text='Выберите: ',
        reply_markup=reply_markup,
    )
    return HANDLE_EVENT


def show_event_details(update, context):
    event_id = update.callback_query.data
    message = get_message(event_id)
    keyboard = [
        [InlineKeyboardButton('Назад', callback_data='Назад')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=message,
        reply_markup=reply_markup,
    )
    return HANDLE_EVENT


def cancel(update, context):
    update.message.reply_text(
        'Всего доброго!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def bot_starting():
    TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    conversation = ConversationHandler(
        entry_points=[CommandHandler('start', show_menu)],
        states={
            HANDLE_MENU: [
                CallbackQueryHandler(show_meetups, pattern=r'Программа'),
                CallbackQueryHandler(question_show_meetups,
                                     pattern=r'Задать вопрос'),
            ],
            HANDLE_MEETUP: [
                CallbackQueryHandler(
                    show_event, pattern=r'[0-9]'
                ),
                CallbackQueryHandler(
                    question_show_event, pattern=r'^AQ_[0-9]*$'
                ),
                CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
            ],
            HANDLE_EVENT: [
                CallbackQueryHandler(show_event_details, pattern=r'[0-9]'),
                CallbackQueryHandler(show_meetups, pattern=r'Назад'),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conversation)

    updater.start_polling()


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **options):
        bot_starting()
