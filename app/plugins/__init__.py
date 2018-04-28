import importlib


class Plugin(object):
    MESSAGE_FIELDS = []

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def get_any_text(self, update):
        return list(filter(None, [
            update.message.text,
            update.message.caption,
        ]))

    def process_update(self, bot, update, db_update):
        pass

    @classmethod
    def load(cls, app, modname):
        modname, pluginclsname = modname.rsplit('.', 1)
        mod = importlib.import_module(modname)
        plugincls = getattr(mod, pluginclsname)
        return plugincls(app)


class PluginProcessor(object):
    def __init__(self, app):
        self.app = app
        self.plugins = []
        for mod in self.app.config['PLUGINS']:
            self.plugins.append(Plugin.load(self.app, mod))

    def process_update(self, bot, update):
        # TODO: create db_update from update
        db_update = None
        for plugin in self.plugins:
            plugin.process_update(bot, update, db_update)

        return db_update
