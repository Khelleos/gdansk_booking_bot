from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import BOOKING_SITE_URL
from bot.i18n import messages
from bot.i18n.locales import LANGUAGES

CHECK_CALLBACK = "check"
LANGUAGE_CALLBACK_PREFIX = "lang:"

LANGUAGE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(name, callback_data=f"{LANGUAGE_CALLBACK_PREFIX}{code}")]
     for code, name in LANGUAGES.items()]
)


def bot_commands(lang):
    return [BotCommand(command, description) for command, description in messages.command_descriptions(lang)]


def open_site_button(lang):
    return InlineKeyboardButton(messages.open_site_button(lang), url=BOOKING_SITE_URL)


def check_again_button(lang):
    return InlineKeyboardButton(messages.check_again_button(lang), callback_data=CHECK_CALLBACK)
