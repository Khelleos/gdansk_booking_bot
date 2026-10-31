"""Translated text, one module per language, collected into lookup tables.

STRINGS values are str.format templates. Tuples are plural forms: (one, other) for
English, (one, few, many) for the Slavic languages. Keep the keys in all languages in
sync; a missing key falls back to English. To add a language, add its module here.
"""
from bot.i18n.locales import be, en, pl, ru, uk

DEFAULT_LANGUAGE = "en"

# Order is the order of the /language picker
_LOCALES = {"en": en, "pl": pl, "ru": ru, "uk": uk, "be": be}

LANGUAGES = {code: locale.NAME for code, locale in _LOCALES.items()}
MONTHS = {code: locale.MONTHS for code, locale in _LOCALES.items()}
WEEKDAYS = {code: locale.WEEKDAYS for code, locale in _LOCALES.items()}
STRINGS = {code: locale.STRINGS for code, locale in _LOCALES.items()}
