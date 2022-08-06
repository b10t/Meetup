import logging

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from tgbot.management.commands._tools import States, get_meetups

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def show_meetups(update: Update, context: CallbackContext):
    """Отображает список митапов."""
    context.user_data[States.START_OVER] = True
    keyboard = list()
    meetups = get_meetups()
    for meetup in meetups:
        keyboard.append(
            [InlineKeyboardButton(meetup.name, callback_data=meetup.id)]
        )
    keyboard.append(
        [InlineKeyboardButton('Главное меню', callback_data='Главное меню')]
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text='Выберете митап:',
        reply_markup=keyboard
    )

    return States.BACK_TO_MAIN_MENU


conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            show_meetups,
            pattern='^' + 'SHOW_MEETUPS' + '$'
        )
    ],
    states={
    },
    fallbacks=[
    ],
    map_to_parent={
        States.BACK_TO_MAIN_MENU: States.BACK_TO_MAIN_MENU,
    },
)
