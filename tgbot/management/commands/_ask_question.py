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

STOPPING, SHOWING = map(chr, range(8, 10))


def show_meetups(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        f'ASK_QUESTION'
    )

    return STOPPING


question_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        show_meetups, pattern="^ASK_QUESTION")],  # type: ignore
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
        STOPPING: STOPPING,
    },
)
