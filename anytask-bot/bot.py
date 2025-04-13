import functools
import logging

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import ParseMode

from constants import (ANYTASK_LOGIN, ANYTASK_PASSWORD, DEBUG_API, RELEASE_API)
from anytask_client import AnytaskClient
from decorators import send_typing_action


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


updater = Updater(token=DEBUG_API, use_context=True)
dispatcher = updater.dispatcher

ac = AnytaskClient(ANYTASK_LOGIN, ANYTASK_PASSWORD)


def start_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Я умею приносить данные из ведомости Anytask.")


@send_typing_action
def final_command(update, context):
    logging.info('"final" command called')
    message = ac.final_grade_report()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message,
                             parse_mode=ParseMode.MARKDOWN_V2)


@send_typing_action
def sum_command(update, context):
    logging.info('"sum" command called')
    message = ac.sum_grade_report()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message,
                             parse_mode=ParseMode.MARKDOWN_V2)


@send_typing_action
def done_command(update, context):
    logging.info('"done" command called')
    message = ac.done_report()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message,
                             parse_mode=ParseMode.MARKDOWN_V2)


@send_typing_action
def group_command(update, context):
    logging.info('"check" command called')
    subm, nsubm, verif = ac.group_stats()
    message = (f'Отправлено: *{subm}*\n' f'Не отправлено: *{nsubm}*\n'
               f'Проверено: *{verif}*')

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message, parse_mode=ParseMode.MARKDOWN_V2)


def unknown(update, context):
    logging.info('"unknown" comman called')
    # chivo_pic = https://memepedia.ru/wp-content/uploads/2019/08/screenshot_17-2.png
    # context.bot.send_photo(chat_id=update.effective_chat.id,
    #                       photo=chivo_pic)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Я не знаю такой команды.")


start_handler = CommandHandler('start', start_command)
dispatcher.add_handler(start_handler)

check_handler = CommandHandler('group', group_command)
dispatcher.add_handler(check_handler)

final_handler = CommandHandler('final', final_command)
dispatcher.add_handler(final_handler)

done_handler = CommandHandler('done', done_command)
dispatcher.add_handler(done_handler)

sum_handler = CommandHandler('sum', sum_command)
dispatcher.add_handler(sum_handler)


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
