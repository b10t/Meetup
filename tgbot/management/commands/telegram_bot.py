from django.conf import settings
from django.core.management.base import BaseCommand
from telegram import (ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      ParseMode, ReplyKeyboardRemove, Update, chat)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils import helpers


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

    user_id = update.message.chat_id
    context.user_data['user_id'] = user_id
    first_name = update.message.chat.first_name

    if update.message.chat.last_name:
        context.user_data['last_name'] = update.message.chat.last_name
    else:
        context.user_data['last_name'] = ''

    # database_user_id = Player.objects.filter(chat_id=user_id)
    # if not database_user_id:
    #     Player.objects.create(
    #         chat_id=user_id,
    #         firs_name=first_name,
    #         last_name=context.user_data['last_name'],
    #     )

    update.message.reply_text(
        f'Здравствуйте, {first_name}\.\n'
        'Это официальный бот по поддержке участников\. 🤖 \n',
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=inl_keyboard
    )
    return 'callback_select_main_menu'


def callback_select_main_menu(update: Update, context: CallbackContext):
    """."""
    bot = update.effective_message.bot
    query = update.callback_query

    # if query.data == 'CREATE_GAME':
    #     return send_gamename_question(update, context)
    # elif query.data == 'JOIN_THE_GAME':
    #     return choose_game(update, context)
    # else:
    #     return ConversationHandler.END

    ConversationHandler.END


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
            entry_points=[CommandHandler('start', start_handler)],  # type: ignore
            states={
                'callback_select_main_menu': [
                    CallbackQueryHandler(
                        callback_select_main_menu
                    )
                ]
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
