"""Builds the text of every bot message in the requested language."""
import html
from datetime import datetime

from bot.i18n.translations import DEFAULT_LANGUAGE, LANGUAGES, MONTHS, STRINGS, WEEKDAYS

# Telegram rejects messages over 4096 characters; leave room for the header and footer
MAX_SLOTS_TEXT_LENGTH = 3500


def detect_language(language_code) -> str:
    """Map a Telegram language_code ("pl", "uk-UA", ...) to a supported language."""
    if language_code:
        code = language_code.split('-')[0].lower()
        if code in LANGUAGES:
            return code
    return DEFAULT_LANGUAGE


def _text(lang: str, key: str, **kwargs) -> str:
    template = STRINGS.get(lang, {}).get(key) or STRINGS[DEFAULT_LANGUAGE][key]
    return template.format(**kwargs)


def _plural_index(lang: str, n: int) -> int:
    if lang == "en":
        return 0 if n == 1 else 1
    if lang == "pl":
        if n == 1:
            return 0
    elif n % 10 == 1 and n % 100 != 11:
        return 0
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return 1
    return 2


def _plural(lang: str, key: str, n: int, **kwargs) -> str:
    if lang not in STRINGS or key not in STRINGS[lang]:
        lang = DEFAULT_LANGUAGE
    forms = STRINGS[lang][key]
    return forms[_plural_index(lang, n)].format(n=n, **kwargs)


def command_descriptions(lang: str) -> list:
    """(command, description) pairs for the Telegram command menu."""
    return [
        ("start", _text(lang, "cmd_start")),
        ("check", _text(lang, "cmd_check")),
        ("status", _text(lang, "cmd_status")),
        ("language", _text(lang, "cmd_language")),
        ("stop", _text(lang, "cmd_stop")),
    ]


def open_site_button(lang: str) -> str:
    return _text(lang, "btn_open_site")


def check_again_button(lang: str) -> str:
    return _text(lang, "btn_check_again")


def welcome(lang: str) -> str:
    return _text(lang, "welcome")


def unsubscribed(lang: str) -> str:
    return _text(lang, "unsubscribed")


def not_subscribed(lang: str) -> str:
    return _text(lang, "not_subscribed")


def checking(lang: str) -> str:
    return _text(lang, "checking")


def check_error(lang: str, error: str) -> str:
    return _text(lang, "check_error", error=html.escape(error))


def choose_language(lang: str) -> str:
    return _text(lang, "choose_language")


def language_set(lang: str) -> str:
    return _text(lang, "language_set")


def format_date(lang: str, date: str) -> str:
    try:
        d = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return date
    weekdays = WEEKDAYS.get(lang, WEEKDAYS[DEFAULT_LANGUAGE])
    months = MONTHS.get(lang, MONTHS[DEFAULT_LANGUAGE])
    return f"{weekdays[d.weekday()]}, {d.day} {months[d.month - 1]} {d.year}"


def format_slots(lang: str, slots: dict) -> str:
    """Render slots as HTML: one bold date per block, times in a collapsed blockquote."""
    parts = []
    length = 0
    for i, (date, times) in enumerate(slots.items()):
        title = html.escape(format_date(lang, date))
        if times:
            times_text = "\n".join(html.escape(t) for t in times)
            part = (
                f"<b>{title}</b> · {_plural(lang, 'slots_count', len(times))}\n"
                f"<blockquote expandable>{times_text}</blockquote>"
            )
        else:
            part = f"<b>{title}</b>\n{_text(lang, 'times_unavailable')}"
        if length + len(part) > MAX_SLOTS_TEXT_LENGTH:
            parts.append(_plural(lang, 'more_dates', len(slots) - i))
            break
        parts.append(part)
        length += len(part)
    return "\n\n".join(parts)


def format_duration(lang: str, seconds: float) -> str:
    minutes = round(seconds / 60)
    if minutes < 1:
        return _text(lang, "less_than_minute")
    return _text(lang, "duration_min", n=minutes)


def availability_alert(lang: str, slots: dict, found_at: datetime) -> str:
    return (
        f"{_text(lang, 'alert_title')}\n\n"
        f"{_text(lang, 'alert_body')}\n\n"
        f"{format_slots(lang, slots)}\n\n"
        f"{_text(lang, 'found_at', time=found_at.strftime('%Y-%m-%d %H:%M:%S'))}"
    )


def check_result(lang: str, slots: dict, checked_at: datetime) -> str:
    checked = _text(lang, "checked_at", time=checked_at.strftime('%H:%M:%S'))
    if slots:
        return f"{_text(lang, 'slots_available')}\n\n{format_slots(lang, slots)}\n\n{checked}"
    return f"{_text(lang, 'no_slots')}\n\n{checked}"


def check_result_label(lang: str, result: str, dates: int = 0) -> str:
    """Short label for the last background check; `result` is found/none/timeout/error."""
    if result == "found":
        return _text(lang, "result_found", dates=_plural(lang, "dates_count", dates))
    return _text(lang, f"result_{result}")


def status(lang: str, is_subscribed: bool, total: int, last_check_at, last_result,
           next_check_at, now: datetime) -> str:
    """`last_result` is a (result, dates) pair for check_result_label; `next_check_at` is a timestamp."""
    if last_check_at:
        last_check = _text(
            lang, "ago",
            duration=format_duration(lang, (now - last_check_at).total_seconds()),
            result=check_result_label(lang, *last_result),
        )
    else:
        last_check = _text(lang, "not_yet")
    if next_check_at:
        next_check = _text(
            lang, "in_about",
            duration=format_duration(lang, max(0, next_check_at - now.timestamp())),
        )
    else:
        next_check = _text(lang, "unknown")

    return (
        f"{_text(lang, 'status_title')}\n\n"
        f"{_text(lang, 'status_subscribed', value=_text(lang, 'yes' if is_subscribed else 'no'))}\n"
        f"{_text(lang, 'status_total', n=total)}\n"
        f"{_text(lang, 'status_last_check', value=last_check)}\n"
        f"{_text(lang, 'status_next_check', value=next_check)}"
    )
