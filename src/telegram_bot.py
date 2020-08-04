from telegram import Bot, Update, Message, User
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler


class CommandRequest(object):
    def __init__(self, update: Update, context: CallbackContext):
        self._update = update
        self._context = context

    @property
    def message(self) -> Message:
        return self._update.message

    @property
    def user(self) -> User:
        return self._update.effective_user


class TelegramBot(object):
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self):
        def default_start(request: CommandRequest):
            self.reply_message(request.message, "It's me, TelegramBot!")

        self.register_command('start', default_start)
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def register_command(self, command_name, command_callback):
        command_handler = _command_handler_builder(command_callback)
        self.dispatcher.add_handler(CommandHandler(command_name, command_handler))

    def command(self, command_name):
        def declare_command_decorator(command_callback):
            self.register_command(command_name, command_callback)
            return command_callback
        return declare_command_decorator

    def send_message(self, chat_id, text):
        self.bot.send_message(chat_id, text)

    def reply_message(self, message: Message, text):
        self.bot.send_message(message.chat_id, text)


def _command_handler_builder(command_callback):
    def command_handler(update, context):
        command_callback(CommandRequest(update, context))

    return command_handler
