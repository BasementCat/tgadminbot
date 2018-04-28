from . import Plugin


class Stdout(Plugin):
    def process_update(self, bot, update, db_update):
        print(update)
