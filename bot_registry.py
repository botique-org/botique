_bot_registry = {}


def register_bot(bot_name, bot_class):
    _bot_registry[bot_name.lower()] = bot_class


def get_bot(bot_name):
    return _bot_registry.get(bot_name.lower())
