import datetime
from functools import wraps

from telegram import ChatAction


def cache(ttl=datetime.timedelta(minutes=10)):
    def wrap(func):
        cache = {}
        @wraps(func)
        def wrapped(*args, **kw):
            now = datetime.datetime.now()
            key = tuple(args), frozenset(kw.items())
            if key not in cache or now - cache[key][0] > ttl:
                value = func(*args, **kw)
                cache[key] = (now, value)
            return cache[key][1]
        return wrapped
    return wrap

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func