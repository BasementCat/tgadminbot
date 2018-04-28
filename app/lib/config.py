import os
import json


CANDIDATE_CONFIG_FILES = [
    './config.json',
    '~/.config/tgadminbot/config.json',
    '~/.config/tgadminbot-config.json',
    '~/.tgadminbot-config.json',
    '/etc/tgadminbot/config.json',
    '/etc/tgadminbot-config.json',
]


def load_config(config_file=None):
    candidates = [config_file] if config_file else CANDIDATE_CONFIG_FILES
    for candidate in candidates:
        fname = os.path.normpath(os.path.abspath(os.path.expanduser(candidate)))
        if os.path.exists(fname):
            with open(fname, 'r') as fp:
                return json.load(fp)

    raise RuntimeError("No config file found at " + ', '.join(candidates))
