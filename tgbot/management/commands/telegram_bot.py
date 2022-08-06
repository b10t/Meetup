import logging
import threading

import tgbot.management.commands._ask_question as ask_question
import tgbot.management.commands._show_meetups as show_meetups
from django.conf import settings
from django.core.management.base import BaseCommand
from event.models import Participant
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ReplyKeyboardRemove, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Updater)
from tgbot.management.commands._tools import States

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# HANDLE_MENU, HANDLE_MEETUP = range(2)


# def show_menu(update, context):
#     bot = context.bot
#     user_id = update.effective_user.id
#     keyboard = [
#         [InlineKeyboardButton('Программа', callback_data='Программа')],
#         [InlineKeyboardButton('Задать вопрос', callback_data='Задать вопрос')],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     bot.send_message(
#         text='Здравствуйте! Это официальный бот по поддержке участников.',
#         chat_id=user_id,
#         reply_markup=reply_markup,
#     )
#     return HANDLE_MENU


# def show_meetups(update, context):
#     meetups = get_meetups()
#     keyboard = list()
#     for meetup in meetups:
#         keyboard.append(
#             [InlineKeyboardButton(meetup, callback_data=meetup)]
#         )
#     keyboard.append(
#         [InlineKeyboardButton(
#             'Главное меню',
#             callback_data='Главное меню',
#         )]
#     )
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.callback_query.answer()
#     update.callback_query.edit_message_text(
#         text='Выберите', reply_markup=reply_markup
#     )
#     return HANDLE_MEETUP

def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg="Exception while handling an update:",
        exc_info=context.error
    )


def start_handler(update: Update, context: CallbackContext):
    text = f'Выберете действие:'

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

    if context.user_data.get(States.START_OVER):
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
            reply_markup=inl_keyboard
        )

    context.user_data[States.START_OVER] = False

    return States.SHOW_MEETUPS


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel and end the conversation."""

    update.message.reply_text(
        'Всего доброго!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def bot_starting():
    TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN

    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conversation = ConversationHandler(
        name='main_conv',
        entry_points=[CommandHandler(
            'start', start_handler)],  # type: ignore
        states={
            States.BACK_TO_MAIN_MENU: [CallbackQueryHandler(start_handler, pattern='^BACK_TO_MAIN_MENU$')],
            States.SHOW_MEETUPS: [
                show_meetups.conversation,
                ask_question.conversation
            ],
        },  # type: ignore
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('stop', cancel)
        ],  # type: ignore

    )

    # conversation = ConversationHandler(
    #     entry_points=[CommandHandler('start', show_menu)],
    #     states={
    #         HANDLE_MENU: [
    #             CallbackQueryHandler(show_meetups, pattern=r'Программа'),
    #         ],
    #         HANDLE_MEETUP: [
    #             CallbackQueryHandler(
    #                 show_meetups, pattern=r'Вступительные мероприятия'
    #             ),
    #             CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
    #         ],
    #     },
    #     fallbacks=[
    #         CommandHandler('cancel', cancel)],
    # )

    dispatcher.add_handler(conversation)

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    # updater.idle()


class Command(BaseCommand):
    """Start the bot."""

    help = "Телеграм-бот"

    def handle(self, *args, **options):
        threading.Thread(target=bot_starting).start()
