#!/usr/bin/env python3
from time import sleep

from telegram_bot import TelegramBot, CommandRequest

bot = TelegramBot('')


@bot.command('test')
def do_test(request: CommandRequest):
    bot.reply_message(request.message, 'This is a test')
    bot.send_message(request.message.chat_id, 'I can use chat_id for send messages too')
    bot.reply_message(request.message, f'I know you very well, {request.user.name}.')


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
