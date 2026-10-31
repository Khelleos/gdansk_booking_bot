# Native name, shown in the /language picker
NAME = "Русский"

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]

# Short weekday names, Monday first
WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]

STRINGS = {
    "cmd_start": "Включить уведомления",
    "cmd_check": "Проверить наличие мест сейчас",
    "cmd_status": "Статус бота и время следующей проверки",
    "cmd_stop": "Отключить уведомления",
    "cmd_language": "Сменить язык",
    "btn_open_site": "📅 Открыть сайт записи",
    "btn_check_again": "🔄 Проверить снова",
    "welcome": (
        "👋 Добро пожаловать в бот мониторинга записи в Гданьске!\n\n"
        "Я сообщу, когда появятся свободные места для записи.\n\n"
        "Команды (также в кнопке Меню):\n"
        "/start - Включить уведомления\n"
        "/stop - Отключить уведомления\n"
        "/check - Проверить наличие мест сейчас\n"
        "/status - Статус бота\n"
        "/language - Сменить язык"
    ),
    "unsubscribed": "Вы отписались от уведомлений.",
    "not_subscribed": "Вы не подписаны на уведомления.",
    "checking": "🔍 Проверяю наличие мест...",
    "check_error": "❌ Ошибка при проверке: {error}",
    "checked_at": "<i>Проверено в {time}</i>",
    "slots_available": "✅ <b>Есть свободные места для записи!</b>",
    "no_slots": "❌ Сейчас свободных мест нет.",
    "alert_title": "🎉 <b>Появились свободные места!</b>",
    "alert_body": "В Поморском воеводском управлении в Гданьске появились новые места для записи.",
    "found_at": "<i>Найдено: {time}</i>",
    "slots_count": ("{n} слот", "{n} слота", "{n} слотов"),
    "dates_count": ("{n} дата", "{n} даты", "{n} дат"),
    "times_unavailable": "<i>время недоступно</i>",
    "more_dates": ("<i>…и ещё {n} дата на сайте</i>",
                   "<i>…и ещё {n} даты на сайте</i>",
                   "<i>…и ещё {n} дат на сайте</i>"),
    "duration_min": "{n} мин",
    "less_than_minute": "меньше минуты",
    "status_title": "🤖 <b>Статус бота</b>",
    "status_subscribed": "Подписка: {value}",
    "status_total": "Всего подписчиков: {n}",
    "status_last_check": "Последняя проверка: {value}",
    "status_next_check": "Следующая проверка: {value}",
    "yes": "✅ Да",
    "no": "❌ Нет",
    "ago": "{duration} назад — {result}",
    "not_yet": "ещё не было",
    "in_about": "через ~{duration}",
    "unknown": "неизвестно",
    "result_found": "✅ найдены места ({dates})",
    "result_none": "мест нет",
    "result_timeout": "⚠️ превышено время ожидания",
    "result_error": "⚠️ ошибка",
    "choose_language": "🌐 Выберите язык:",
    "language_set": "✅ Выбран русский язык.",
}
