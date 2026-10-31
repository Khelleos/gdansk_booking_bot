import unittest
from datetime import datetime, timedelta

from bot.i18n import messages
from bot.i18n.locales import DEFAULT_LANGUAGE, LANGUAGES, MONTHS, STRINGS, WEEKDAYS

NOW = datetime(2026, 11, 2, 12, 0, 0)
SLOTS = {"2026-11-05": ["09:00", "09:40"], "2026-11-06": ["10:00"], "2026-11-07": []}


class LocalesTest(unittest.TestCase):
    def test_every_language_has_the_same_keys(self):
        for lang in LANGUAGES:
            with self.subTest(lang=lang):
                self.assertEqual(set(STRINGS[lang]), set(STRINGS[DEFAULT_LANGUAGE]))

    def test_plural_forms_have_the_right_count(self):
        for lang in LANGUAGES:
            expected = 2 if lang == "en" else 3
            for key, value in STRINGS[lang].items():
                if isinstance(value, tuple):
                    with self.subTest(lang=lang, key=key):
                        self.assertEqual(len(value), expected)

    def test_calendar_names(self):
        for lang in LANGUAGES:
            with self.subTest(lang=lang):
                self.assertEqual(len(MONTHS[lang]), 12)
                self.assertEqual(len(WEEKDAYS[lang]), 7)


class PluralTest(unittest.TestCase):
    def forms(self, lang, numbers):
        return [messages._plural(lang, "slots_count", n) for n in numbers]

    def test_english(self):
        self.assertEqual(self.forms("en", [1, 2, 11]), ["1 slot", "2 slots", "11 slots"])

    def test_polish(self):
        self.assertEqual(
            self.forms("pl", [1, 2, 5, 12, 21, 22]),
            ["1 termin", "2 terminy", "5 terminów", "12 terminów", "21 terminów", "22 terminy"],
        )

    def test_russian(self):
        self.assertEqual(
            self.forms("ru", [1, 2, 5, 11, 21, 22]),
            ["1 слот", "2 слота", "5 слотов", "11 слотов", "21 слот", "22 слота"],
        )


class DetectLanguageTest(unittest.TestCase):
    def test_detection(self):
        self.assertEqual(messages.detect_language("uk-UA"), "uk")
        self.assertEqual(messages.detect_language("PL"), "pl")
        self.assertEqual(messages.detect_language("de"), "en")
        self.assertEqual(messages.detect_language(None), "en")


class RenderTest(unittest.TestCase):
    def test_every_message_renders_in_every_language(self):
        for lang in LANGUAGES:
            with self.subTest(lang=lang):
                messages.welcome(lang)
                messages.unsubscribed(lang)
                messages.not_subscribed(lang)
                messages.checking(lang)
                messages.choose_language(lang)
                messages.language_set(lang)
                messages.command_descriptions(lang)
                messages.availability_alert(lang, SLOTS, NOW)
                messages.check_result(lang, SLOTS, NOW)
                messages.check_result(lang, {}, NOW)
                messages.status(lang, True, 3, NOW - timedelta(minutes=4), ("found", 2), NOW.timestamp() + 300, NOW)
                messages.status(lang, False, 0, None, None, None, NOW)
                for result in ("none", "timeout", "error"):
                    messages.check_result_label(lang, result)

    def test_dates(self):
        self.assertEqual(messages.format_date("en", "2026-11-05"), "Thu, 5 Nov 2026")
        self.assertEqual(messages.format_date("pl", "2026-11-05"), "czw., 5 listopada 2026")
        self.assertEqual(messages.format_date("en", "not a date"), "not a date")

    def test_error_text_is_escaped(self):
        self.assertIn("&lt;html&gt;", messages.check_error("en", "<html>"))

    def test_long_slot_lists_are_cut(self):
        slots = {f"2026-12-{day:02d}": [f"{h:02d}:00" for h in range(8, 18)] * 3 for day in range(1, 32)}
        text = messages.format_slots("ru", slots)
        self.assertLess(len(text), 4096)
        self.assertIn("…и ещё", text)
