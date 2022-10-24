from telegram import update
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

import logging
import telegram
#import cript

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

bot = telegram.Bot(token='2048881693:AAHTWGVj26XT_KIH3E5dNjuVAfweQKr1IiI')


def chat_id_uniq():
    with open('chat_id.txt') as result:
        uniqlines = set(result.readlines())
        with open('chat_id_uniq.txt', 'w') as rmdup:
            rmdup.writelines(set(uniqlines))


def start(update, context):
    f = open('chat_id.txt', 'a')
    chat_id = update.message.chat_id
    f.write(str(chat_id) + '\n')
    chat_id_uniq()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Добро пожаловать в мир Новой монетки!")

    #context.job_queue.run_repeating(callback_minute, interval=300, first=5,
                                   # context=update.message.chat_id)


def callback_minute(context):
    chat_ids = set(open('chat_id_uniq.txt').readlines())
    import cript
    for chat_id in chat_ids:

        context.bot.send_message(chat_id=chat_id,
                                 text=cript.checking())
    cript.rename_file()


def main():
    updater = Updater(token='2048881693:AAHTWGVj26XT_KIH3E5dNjuVAfweQKr1IiI', use_context=True)
    dp = updater.dispatcher
    updater.job_queue.run_repeating(callback_minute, interval=1800, first=5)
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
