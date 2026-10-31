# Native name, shown in the /language picker
NAME = "Українська"

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = [
    "січня", "лютого", "березня", "квітня", "травня", "червня",
    "липня", "серпня", "вересня", "жовтня", "листопада", "грудня",
]

# Short weekday names, Monday first
WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "нд"]

STRINGS = {
    "cmd_start": "Увімкнути сповіщення",
    "cmd_check": "Перевірити наявність місць зараз",
    "cmd_status": "Статус бота і час наступної перевірки",
    "cmd_stop": "Вимкнути сповіщення",
    "cmd_language": "Змінити мову",
    "btn_open_site": "📅 Відкрити сайт запису",
    "btn_check_again": "🔄 Перевірити ще раз",
    "welcome": (
        "👋 Вітаємо в боті моніторингу запису в Гданську!\n\n"
        "Я повідомлю, коли з'являться вільні місця для запису.\n\n"
        "Команди (також у кнопці Меню):\n"
        "/start - Увімкнути сповіщення\n"
        "/stop - Вимкнути сповіщення\n"
        "/check - Перевірити наявність місць зараз\n"
        "/status - Статус бота\n"
        "/language - Змінити мову"
    ),
    "unsubscribed": "Ви відписалися від сповіщень.",
    "not_subscribed": "Ви не підписані на сповіщення.",
    "checking": "🔍 Перевіряю наявність місць...",
    "check_error": "❌ Помилка під час перевірки: {error}",
    "checked_at": "<i>Перевірено о {time}</i>",
    "slots_available": "✅ <b>Є вільні місця для запису!</b>",
    "no_slots": "❌ Наразі вільних місць немає.",
    "alert_title": "🎉 <b>З'явилися вільні місця!</b>",
    "alert_body": "У Поморському воєводському управлінні в Гданську з'явилися нові місця для запису.",
    "found_at": "<i>Знайдено: {time}</i>",
    "slots_count": ("{n} слот", "{n} слоти", "{n} слотів"),
    "dates_count": ("{n} дата", "{n} дати", "{n} дат"),
    "times_unavailable": "<i>час недоступний</i>",
    "more_dates": ("<i>…і ще {n} дата на сайті</i>",
                   "<i>…і ще {n} дати на сайті</i>",
                   "<i>…і ще {n} дат на сайті</i>"),
    "duration_min": "{n} хв",
    "less_than_minute": "менше хвилини",
    "status_title": "🤖 <b>Статус бота</b>",
    "status_subscribed": "Підписка: {value}",
    "status_total": "Усього підписників: {n}",
    "status_last_check": "Остання перевірка: {value}",
    "status_next_check": "Наступна перевірка: {value}",
    "yes": "✅ Так",
    "no": "❌ Ні",
    "ago": "{duration} тому — {result}",
    "not_yet": "ще не було",
    "in_about": "через ~{duration}",
    "unknown": "невідомо",
    "result_found": "✅ знайдено місця ({dates})",
    "result_none": "місць немає",
    "result_timeout": "⚠️ перевищено час очікування",
    "result_error": "⚠️ помилка",
    "choose_language": "🌐 Оберіть мову:",
    "language_set": "✅ Обрано українську мову.",
}
