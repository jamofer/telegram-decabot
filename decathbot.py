#!/usr/bin/env python3
from time import sleep

from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot import TelegramBot


bot = TelegramBot('')


@bot.command('test')
def do_test(update: Update, context: CallbackContext):
    update.message.reply_text('Test reply')
    chat_id = update.message.chat_id
    bot.send_message(chat_id, 'Test send message using chat_id')


if __name__ == '__main__':
    bot.start()
    print('Bot has been started')
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print('Stopping...')
        bot.stop()

    exit(0)
