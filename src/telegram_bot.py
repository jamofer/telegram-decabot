from functools import wraps

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler


class TelegramBot(object):
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self):
        self.dispatcher.add_handler(CommandHandler('start', default_start))
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def register_command(self, command_name, command_callback):
        self.dispatcher.add_handler(CommandHandler(command_name, command_callback))

    def command(self, command_name):
        def declare_command_decorator(command_callback):
            self.register_command(command_name, command_callback)
            return command_callback
        return declare_command_decorator

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)


def default_start(update, context):
    update.message.reply_text("It's me, TelegramBot!")
