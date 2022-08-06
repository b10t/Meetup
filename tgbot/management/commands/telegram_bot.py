import logging
import threading
from django.conf import settings
from django.core.management.base import BaseCommand

from tgbot.management.commands._tools import get_meetups
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Updater
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


HANDLE_MENU, HANDLE_MEETUP = range(2)


def show_menu(update, context):
    bot = context.bot
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton('Программа', callback_data='Программа')],
        [InlineKeyboardButton('Задать вопрос', callback_data='Задать вопрос')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        text='Здравствуйте! Это официальный бот по поддержке участников.',
        chat_id=user_id,
        reply_markup=reply_markup,
    )
    return HANDLE_MENU


def show_meetups(update, context):
    meetups = get_meetups()
    keyboard = list()
    for meetup in meetups:
        keyboard.append(
            [InlineKeyboardButton(meetup, callback_data=meetup)]
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
        text='Выберите', reply_markup=reply_markup
    )
    return HANDLE_MEETUP


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
        entry_points=[CommandHandler('start', show_menu)],
        states={
            HANDLE_MENU: [
                CallbackQueryHandler(show_meetups, pattern=r'Программа'),
            ],
            HANDLE_MEETUP: [
                CallbackQueryHandler(
                    show_meetups, pattern=r'Вступительные мероприятия'
                ),
                CallbackQueryHandler(show_menu, pattern=r'Главное меню'),
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel)],  # type: ignore
    )

    dispatcher.add_handler(conversation)

    updater.start_polling()
    # updater.idle()


class Command(BaseCommand):
    """Start the bot."""

    help = "Телеграм-бот"

    def handle(self, *args, **options):
        threading.Thread(target=bot_starting).start()
