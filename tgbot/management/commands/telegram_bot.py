import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from event.models import Participant

from ._tools import (
    get_meetups,
    get_event,
    get_message,
    save_question,
)

from ._tools import (
    get_meetups,
    get_event,
    get_event_speker,
    get_speaker,
)
from event.models import LISTENER, SPEAKER
from ._botfunctions import (
    get_event_participants,
)
# from ._ask_question import (
#     question_show_meetups,
#     question_show_event,

# )
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
    MessageHandler,
    Filters,
    Updater,
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
    START_OVER,
    HANDLE_QUESTIONS,
    HANDLE_SPEAKER_QUESTIONS,
    HANDLE_TYPE_MESSAGE,
) = range(7)


def show_menu(update, context):
    logger.info('show_menu')
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
            reply_markup=keyboard
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
    logger.info('show_event_details')
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


def show_questions_meetup(update, context):
    logger.info('show_questions_meetup')

    meetups = get_meetups()
    keyboard = list()
    for meetup in meetups:
        keyboard.append(
            [
                InlineKeyboardButton(
                    meetup.name, callback_data=meetup.id
                )
            ]
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
    return HANDLE_QUESTIONS


def show_questions_event(update, context):
    logger.info('show_questions_event')
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
        text=f'Выберите: {events}',
        reply_markup=reply_markup,
    )
    return HANDLE_SPEAKER_QUESTIONS


def show_event_speakers(update, context):
    logger.info('show_event_speakers')
    event_id = update.callback_query.data
    speakers = get_event_participants(event_id, SPEAKER)
    keyboard = list()
    for speaker in speakers:
        keyboard.append(
            [InlineKeyboardButton(
                speaker['fio'],
                callback_data=speaker['tg_id']
                )]
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
    return HANDLE_TYPE_MESSAGE


def type_speaker_message(update, context):
    logger.info('type_speaker_message')

    speaker_tg_id = update.callback_query.data
    bot = context.bot
    user_id = update.effective_user.id
    context.bot_data['speaker_tg_id'] = speaker_tg_id
    bot.send_message(
        text='Введите ваш вопрос спикеру.',
        chat_id=user_id,
    )
    bot.delete_message(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
    )
    return HANDLE_TYPE_MESSAGE


def check_question(update, context):
    logger.info('check_question')

    bot = context.bot
    user_id = update.effective_user.id
    message = update.message.text
    keyboard = [
        [InlineKeyboardButton(
            'Отправить вопрос',
            callback_data='Отправить вопрос'
        )],
        [InlineKeyboardButton('Ввести снова', callback_data='Ввести снова')],
    ]
    context.user_data['message'] = message
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        text=f'Вы ввели: {message}',
        chat_id=user_id,
        reply_markup=reply_markup,
    )
    return HANDLE_TYPE_MESSAGE


def save_question(update, context):
    logger.info('save_question')
    message = context.user_data['message']
    speaker_tg_id = context.bot_data['speaker_tg_id']
    bot = context.bot
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton('Главное меню', callback_data='Главное меню')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    save_question(message, speaker_tg_id)
    bot.send_message(
        chat_id=user_id,
        text='Ваш вопрос отправлен.',
        reply_markup=reply_markup,
    )
    return HANDLE_TYPE_MESSAGE


def show_questions_speaker(update, context):
    logger.info('show_questions_speaker')
    event_id = update.callback_query.data
    event_speakers = get_event_speker(event_id)
    keybord = [
        InlineKeyboardButton('Назад', callback_data='Назад'),
    ]
    reply_markup = InlineKeyboardMarkup(keybord)
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=f'Выберите: {event_speakers}',
        reply_markup=reply_markup,
    )

    return HANDLE_QUESTIONS


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
                CallbackQueryHandler(
                    show_questions_meetup,
                    pattern=r'Задать вопрос'
                ),
            ],
            HANDLE_MEETUP: [
                CallbackQueryHandler(
                    show_event, pattern=r'[0-9]'
                ),
                CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
            ],
            HANDLE_EVENT: [
                CallbackQueryHandler(show_event_details, pattern=r'[0-9]'),
                CallbackQueryHandler(show_meetups, pattern=r'Назад'),
            ],
            HANDLE_QUESTIONS: [
                CallbackQueryHandler(show_questions_event, pattern=r'[0-9]'),
                CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
            ],
            HANDLE_SPEAKER_QUESTIONS: [
                CallbackQueryHandler(show_meetups, pattern=r'Назад'),
                CallbackQueryHandler(show_event_speakers, pattern=r'[0-9]'),
            ],
            HANDLE_TYPE_MESSAGE: [
                CallbackQueryHandler(type_speaker_message, pattern=r'\d+'),
                MessageHandler(
                    Filters.text & ~Filters.command,
                    check_question
                ),
                CallbackQueryHandler(
                    type_speaker_message,
                    pattern=r'Ввести снова'
                ),
                CallbackQueryHandler(
                    save_question,
                    pattern=r'Отправить вопрос'
                ),
                CallbackQueryHandler(show_event_speakers, pattern=r'Назад'),
                CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
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
