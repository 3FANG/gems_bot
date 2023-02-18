from bot import start_bot
from bot.config import load_environment
from bot.payments import get_token

ENV = load_environment()

if __name__ == '__main__':
    if not bool(ENV('YOOMONEY_TOKEN')):
        get_token(ENV('CLIENT_ID'), ENV('REDIRECT_URI'))
    else:
        start_bot()
