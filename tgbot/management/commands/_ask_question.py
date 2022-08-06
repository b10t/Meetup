import logging
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

# import tgbot.management.commands.telegram_bot as telegram_bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BACK_TO_MAIN_MENU, SHOWING = map(chr, range(8, 10))

(
    PARENTS,
    CHILDREN,
    SELF,
    GENDER,
    MALE,
    FEMALE,
    AGE,
    NAME,
    START_OVER,
    FEATURES,
    CURRENT_FEATURE,
    CURRENT_LEVEL,
) = map(chr, range(10, 22))


def show_meetups(update: Update, context: CallbackContext):
    context.user_data[START_OVER] = True

    inl_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    '11',
                    callback_data='1'
                )
            ],
            [
                InlineKeyboardButton(
                    '22',
                    callback_data='1'
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

    return BACK_TO_MAIN_MENU


conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            show_meetups,
            pattern='^' + 'ASK_QUESTION' + '$'
        )
    ],  # type: ignore
    states={
        # "show_period_pm": [MessageHandler(Filters.text & ~Filters.command, show_period_pm)],
        # "change_or_add_period_pm": [MessageHandler(Filters.text & ~Filters.command, change_or_add_period_pm)],
        # "add_period_pm": [MessageHandler(Filters.text & ~Filters.command, add_period_pm)],
        # "edit_period_pm": [MessageHandler(Filters.text & ~Filters.command, edit_period_pm)],
        # "inline_button_change_time": [CallbackQueryHandler(inline_button_change_time, pattern='^TIME_')],
        # "question_change_or_delete_period": [MessageHandler(Filters.text & ~Filters.command, question_change_or_delete_period)],
    },
    fallbacks=[
        # CommandHandler('cancel', cancel)
    ],
    map_to_parent={
        # End everything!
        # ConversationHandler.END: ConversationHandler.END,
        BACK_TO_MAIN_MENU: BACK_TO_MAIN_MENU,
    },
)
