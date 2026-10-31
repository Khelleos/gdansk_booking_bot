# Native name, shown in the /language picker
NAME = "Беларуская"

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = [
    "студзеня", "лютага", "сакавіка", "красавіка", "мая", "чэрвеня",
    "ліпеня", "жніўня", "верасня", "кастрычніка", "лістапада", "снежня",
]

# Short weekday names, Monday first
WEEKDAYS = ["пн", "аў", "ср", "чц", "пт", "сб", "нд"]

STRINGS = {
    "cmd_start": "Уключыць апавяшчэнні",
    "cmd_check": "Праверыць наяўнасць месцаў зараз",
    "cmd_status": "Статус бота і час наступнай праверкі",
    "cmd_stop": "Выключыць апавяшчэнні",
    "cmd_language": "Змяніць мову",
    "btn_open_site": "📅 Адкрыць сайт запісу",
    "btn_check_again": "🔄 Праверыць зноў",
    "welcome": (
        "👋 Вітаем у боце маніторынгу запісу ў Гданьску!\n\n"
        "Я паведамлю, калі з'явяцца вольныя месцы для запісу.\n\n"
        "Каманды (таксама ў кнопцы Меню):\n"
        "/start - Уключыць апавяшчэнні\n"
        "/stop - Выключыць апавяшчэнні\n"
        "/check - Праверыць наяўнасць месцаў зараз\n"
        "/status - Статус бота\n"
        "/language - Змяніць мову"
    ),
    "unsubscribed": "Вы адпісаліся ад апавяшчэнняў.",
    "not_subscribed": "Вы не падпісаны на апавяшчэнні.",
    "checking": "🔍 Правяраю наяўнасць месцаў...",
    "check_error": "❌ Памылка падчас праверкі: {error}",
    "checked_at": "<i>Праверана ў {time}</i>",
    "slots_available": "✅ <b>Ёсць вольныя месцы для запісу!</b>",
    "no_slots": "❌ Зараз вольных месцаў няма.",
    "alert_title": "🎉 <b>З'явіліся вольныя месцы!</b>",
    "alert_body": "У Паморскім ваяводскім упраўленні ў Гданьску з'явіліся новыя месцы для запісу.",
    "found_at": "<i>Знойдзена: {time}</i>",
    "slots_count": ("{n} слот", "{n} слоты", "{n} слотаў"),
    "dates_count": ("{n} дата", "{n} даты", "{n} дат"),
    "times_unavailable": "<i>час недаступны</i>",
    "more_dates": ("<i>…і яшчэ {n} дата на сайце</i>",
                   "<i>…і яшчэ {n} даты на сайце</i>",
                   "<i>…і яшчэ {n} дат на сайце</i>"),
    "duration_min": "{n} хв",
    "less_than_minute": "менш за хвіліну",
    "status_title": "🤖 <b>Статус бота</b>",
    "status_subscribed": "Падпіска: {value}",
    "status_total": "Усяго падпісчыкаў: {n}",
    "status_last_check": "Апошняя праверка: {value}",
    "status_next_check": "Наступная праверка: {value}",
    "yes": "✅ Так",
    "no": "❌ Не",
    "ago": "{duration} таму — {result}",
    "not_yet": "яшчэ не было",
    "in_about": "праз ~{duration}",
    "unknown": "невядома",
    "result_found": "✅ знойдзены месцы ({dates})",
    "result_none": "месцаў няма",
    "result_timeout": "⚠️ перавышаны час чакання",
    "result_error": "⚠️ памылка",
    "choose_language": "🌐 Абярыце мову:",
    "language_set": "✅ Абрана беларуская мова.",
}
