import unittest

from mock import patch, MagicMock
from telegram import Update, Message
from telegram.ext import CallbackContext

from telegram_bot import TelegramBot
from telegram_bot import CommandRequest


class CommandHandlerStub(object):
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback


class TestTelegramBot(unittest.TestCase):
    def setUp(self) -> None:
        self.Updater = patch('telegram_bot.Updater').start()
        self.CommandHandler = patch('telegram_bot.CommandHandler').start()
        self.Bot = patch('telegram_bot.Bot').start()

        self.registered_handlers = []

        self.updater = MagicMock()
        self.Updater.return_value = self.updater

        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler.side_effect = lambda handler: self.registered_handlers.append(handler)

        self.CommandHandler.side_effect = CommandHandlerStub
        self.message = Message(0, None, MagicMock(), MagicMock())

        self.bot = MagicMock()
        self.Bot.return_value = self.bot

    def tearDown(self) -> None:
        patch.stopall()

    def test_it_starts_telegram_bot(self):
        bot = TelegramBot(token='123')

        bot.start()

        self.Updater.assert_called_once_with(token='123', use_context=True)
        self.Bot.assert_called_once_with(token='123')
        self.updater.start_polling.assert_called_once()
        self.expect_command_handler_is_registered('start')

    def test_it_stops_telegram_bot(self):
        bot = TelegramBot(token='123')

        bot.stop()

        self.updater.stop.assert_called_once()

    def test_it_registers_a_command(self):
        def a_command(request: CommandRequest):
            pass
        bot = TelegramBot(token='123')

        bot.register_command('cmd', a_command)

        self.expect_command_handler_is_registered('cmd')

    def test_it_declares_a_function_as_a_bot_command(self):
        bot = TelegramBot(token='123')

        @bot.command('command')
        def a_command(request: CommandRequest):
            pass

        self.expect_command_handler_is_registered('command')

    def test_it_runs_command(self):
        command_callback = MagicMock()
        def a_command(request: CommandRequest):
            command_callback()
        bot = TelegramBot(token='123')
        bot.register_command('command', a_command)

        self.inject_dummy_command('command')

        command_callback.assert_called_once()

    def test_command_request_message(self):
        update = Update(update_id=0, message=self.message)
        context = CallbackContext(self.dispatcher)
        bot = TelegramBot(token='123')

        def a_command(request: CommandRequest):
            assert request.message is update.message
        bot.register_command('command', a_command)

        self.inject_command('command', update, context)

    def test_it_sends_a_message_given_a_chat_id(self):
        bot = TelegramBot(token='123')

        bot.send_message('chat_id', 'message')

        self.bot.send_message.assert_called_once_with('chat_id', 'message')

    def test_it_replies_a_message(self):
        bot = TelegramBot(token='123')

        bot.reply_message(self.message, 'message')

        self.bot.send_message.assert_called_once_with(self.message.chat_id, 'message')

    def expect_command_handler_is_registered(self, name):
        assert any(handler.name == name for handler in self.registered_handlers)

    def inject_command(self, command, update, context):
        for handler in self.registered_handlers:
            if handler.name == command:
                handler.callback(update, context)

    def inject_dummy_command(self, command):
        update = Update(update_id=0)
        context = CallbackContext(self.dispatcher)

        self.inject_command(command, update, context)
