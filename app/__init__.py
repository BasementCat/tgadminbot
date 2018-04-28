import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from app.lib import config
from app.plugins import PluginProcessor


# TODO: do this from config
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('telegram').setLevel(logging.INFO)

logger = logging.getLogger(__name__)


class App(object):
    def __init__(self, config_file=None):
        self.config = config.load_config(config_file=config_file)

        self.updater = Updater(self.config['BOT_TOKEN'])
        self.dispatcher = self.updater.dispatcher
        self.processor = PluginProcessor(self)

        self.register_commands()
        self.register_handlers()

    def register_commands(self):
        for key in ('START_COMMAND_TEXT', 'HELP_COMMAND_TEXT'):
            text = self.config[key]
            if text.startswith('@') and '\n' not in text:
                fname = os.path.normpath(os.path.abspath(os.path.expanduser(text[1:])))
                with open(fname, 'r') as fp:
                    text = fp.read()

            def _send_text(bot, update):
                update.message.reply_text(text)

            self.dispatcher.add_handler(CommandHandler(
                key.split('_')[0].lower(),
                _send_text
            ))

    def register_handlers(self):
        self.dispatcher.add_handler(MessageHandler(None, self.process_message))
        self.dispatcher.add_error_handler(self.process_error)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def process_message(self, bot, update):
        self.processor.process_update(bot, update)

    def process_error(self, bot, update, error):
        logger.error('Update "%s" caused error "%s"', update, error)
