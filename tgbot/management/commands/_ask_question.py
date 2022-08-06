import logging

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from tgbot.management.commands._tools import States, get_meetups

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def show_meetups(update: Update, context: CallbackContext):
    """Отображает список митапов."""
    logger.info('show_meetups')
    context.user_data[States.START_OVER] = True

    inl_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    '11',
                    callback_data='11'
                )
            ],
            [
                InlineKeyboardButton(
                    '22',
                    callback_data='22'
                )
            ],
            [
                InlineKeyboardButton(
                    'Назад',
                    callback_data='BACK_TO_MAIN_MENU'
                )
            ]

        ]
    )

    update.callback_query.answer()
    update.callback_query.edit_message_text(
        text=f'Выберете митап:',
        reply_markup=inl_keyboard
    )

    return States.SELECT_MEETUP


def select_meetup(update: Update, context: CallbackContext):
    logger.info('answer')

    query = update.callback_query
    query.answer()

    data = query.data

    if data == 'BACK_TO_MAIN_MENU':
        return States.BACK_TO_MAIN_MENU

    update.callback_query.edit_message_text(
        "........"
    )

    # update.callback_query.edit_message_text(
    #     text=f'...',
    # )

    # return show_meetups(update, context)

    return States.SHOW_MEETUPS


def fallback(update: Update, context: CallbackContext):
    logger.info('fallback')

    query = update.callback_query
    query.answer()

    data = query.data

    logger.info(data)

    return States.BACK_TO_MAIN_MENU


conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            show_meetups,
            pattern='^' + 'ASK_QUESTION' + '$'
        )
    ],  # type: ignore
    states={
        States.SHOW_MEETUPS: [
            CallbackQueryHandler(show_meetups)
        ],
        States.SELECT_MEETUP: [
            CallbackQueryHandler(fallback, pattern='^BACK_TO_MAIN_MENU$'),
            CallbackQueryHandler(select_meetup),
        ],
        # States.BACK_TO_MAIN_MENU: [
        #     CallbackQueryHandler(fallback, pattern='^BACK_TO_MAIN_MENU$')
        # ],
    },  # type: ignore
    fallbacks=[
        # CallbackQueryHandler(fallback, pattern='')
        # CommandHandler('cancel', cancel)
    ],  # type: ignore
    map_to_parent={
        States.BACK_TO_MAIN_MENU: States.BACK_TO_MAIN_MENU,
    },
)
