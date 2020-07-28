import unittest

import telegram_bot
from mock import patch, MagicMock

from telegram_bot import TelegramBot


class TestTelegramBot(unittest.TestCase):
    def setUp(self) -> None:
        self.Updater = patch('telegram_bot.Updater').start()
        self.CommandHandler = patch('telegram_bot.CommandHandler').start()
        self.Bot = patch('telegram_bot.Bot').start()

        self.updater = MagicMock()
        self.dispatcher = self.updater.dispatcher
        self.Updater.return_value = self.updater

        self.handler = MagicMock()
        self.CommandHandler.return_value = self.handler

        self.bot = MagicMock()
        self.Bot.return_value = self.bot

    def tearDown(self) -> None:
        patch.stopall()

    def test_it_starts_telegram_bot(self):
        bot = TelegramBot(token='123')

        bot.start()

        self.Updater.assert_called_once_with(token='123')
        self.Bot.assert_called_once_with(token='123')
        self.CommandHandler.assert_called_once_with('start', telegram_bot.default_start)
        self.updater.start_polling.assert_called_once()
        self.dispatcher.add_handler.assert_called_once_with(self.handler)

    def test_it_stops_telegram_bot(self):
        bot = TelegramBot(token='123')

        bot.stop()

        self.updater.stop.assert_called_once()

    def test_it_registers_a_command(self):
        def a_command(update, context):
            pass
        bot = TelegramBot(token='123')

        bot.register_command('cmd', a_command)

        self.CommandHandler.assert_called_once_with('cmd', a_command)
        self.dispatcher.add_handler.assert_called_once_with(self.handler)

    def test_it_declares_a_function_as_a_bot_command(self):
        bot = TelegramBot(token='123')

        @bot.command('command')
        def a_command(update, context):
            pass

        self.CommandHandler.assert_called_once_with('command', a_command)
        self.dispatcher.add_handler.assert_called_once_with(self.handler)

    def test_it_sends_a_message_given_a_chat_id(self):
        bot = TelegramBot(token='123')

        bot.send_message('chat_id', 'message')

        self.bot.send_message.assert_called_once_with('chat_id', 'message')
