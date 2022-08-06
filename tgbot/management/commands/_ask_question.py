import logging
import re

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from tgbot.management.commands._tools import get_event, get_meetups

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

HANDLE_MENU, HANDLE_MEETUP, HANDLE_EVENT = range(3)


def question_show_meetups(update: Update, context: CallbackContext):
    logger.info('question_show_meetups')

    meetups = get_meetups()
    keyboard = list()
    for meetup in meetups:
        keyboard.append(
            [
                InlineKeyboardButton(
                    meetup.name, callback_data=f'AQ_{meetup.id}'
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
    return HANDLE_MEETUP


def question_show_event(update: Update, context: CallbackContext):
    logger.info('question_show_event')

    query = update.callback_query

    meetup_id = int(re.sub(r'[\D]', '', query.data))
    events = get_event(meetup_id)
    keyboard = list()
    for event in events:
        keyboard.append(
            [InlineKeyboardButton(event.name, callback_data=f'AQ_{event.id}')]
        )
    keyboard.append(
        [InlineKeyboardButton('Назад', callback_data='AQ_Назад')]
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.answer()
    query.edit_message_text(
        text=f'Выберите: {event}',
        reply_markup=reply_markup,
    )
    return HANDLE_EVENT



# def show_meetups(update: Update, context: CallbackContext):
#     """Отображает список митапов."""
#     context.user_data[States.START_OVER] = True

#     inl_keyboard = InlineKeyboardMarkup(
#         [
#             [
#                 InlineKeyboardButton(
#                     '11',
#                     callback_data='1'
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     '22',
#                     callback_data='1'
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     'Назад',
#                     callback_data='BACK_TO_MAIN_MENU'
#                 )
#             ]

#         ]
#     )

#     update.callback_query.answer()
#     update.callback_query.edit_message_text(
#         text=f'Выберете митап:',
#         reply_markup=inl_keyboard
#     )

#     return States.BACK_TO_MAIN_MENU


# conversation = ConversationHandler(
#     entry_points=[
#         CallbackQueryHandler(
#             show_meetups,
#             pattern='^' + 'ASK_QUESTION' + '$'
#         )
#     ],  # type: ignore
#     states={
#     },
#     fallbacks=[
#         # CommandHandler('cancel', cancel)
#     ],
#     map_to_parent={
#         States.BACK_TO_MAIN_MENU: States.BACK_TO_MAIN_MENU,
#     },
# )
