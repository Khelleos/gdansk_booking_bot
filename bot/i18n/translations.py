"""Translated text for every supported language.

Values are str.format templates. Tuples are plural forms: (one, other) for English,
(one, few, many) for the Slavic languages. Keep the keys in all languages in sync;
a missing key falls back to English.
"""

DEFAULT_LANGUAGE = "en"

# Native names, shown in the /language picker
LANGUAGES = {
    "en": "English",
    "pl": "Polski",
    "ru": "Русский",
    "uk": "Українська",
    "be": "Беларуская",
}

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "pl": ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
           "lipca", "sierpnia", "września", "października", "listopada", "grudnia"],
    "ru": ["января", "февраля", "марта", "апреля", "мая", "июня",
           "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    "uk": ["січня", "лютого", "березня", "квітня", "травня", "червня",
           "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"],
    "be": ["студзеня", "лютага", "сакавіка", "красавіка", "мая", "чэрвеня",
           "ліпеня", "жніўня", "верасня", "кастрычніка", "лістапада", "снежня"],
}

# Short weekday names, Monday first
WEEKDAYS = {
    "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "pl": ["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."],
    "ru": ["пн", "вт", "ср", "чт", "пт", "сб", "вс"],
    "uk": ["пн", "вт", "ср", "чт", "пт", "сб", "нд"],
    "be": ["пн", "аў", "ср", "чц", "пт", "сб", "нд"],
}

STRINGS = {
    "en": {
        "cmd_start": "Start receiving notifications",
        "cmd_check": "Check availability now",
        "cmd_status": "Bot status and next check time",
        "cmd_stop": "Stop receiving notifications",
        "cmd_language": "Change language",
        "btn_open_site": "📅 Open booking site",
        "btn_check_again": "🔄 Check again",
        "welcome": (
            "👋 Welcome to the Gdansk Booking Monitor Bot!\n\n"
            "I will notify you when new appointment slots become available.\n\n"
            "Commands (also in the Menu button):\n"
            "/start - Start receiving notifications\n"
            "/stop - Stop receiving notifications\n"
            "/check - Manually check availability now\n"
            "/status - Check bot status\n"
            "/language - Change language"
        ),
        "unsubscribed": "You have been unsubscribed from notifications.",
        "not_subscribed": "You are not currently subscribed.",
        "checking": "🔍 Checking availability...",
        "check_error": "❌ Error checking availability: {error}",
        "checked_at": "<i>Checked at: {time}</i>",
        "slots_available": "✅ <b>Appointments are available!</b>",
        "no_slots": "❌ No appointments available at the moment.",
        "alert_title": "🎉 <b>Booking Availability Alert!</b>",
        "alert_body": "New appointments are available at Gdansk office.",
        "found_at": "<i>Found at: {time}</i>",
        "slots_count": ("{n} slot", "{n} slots"),
        "dates_count": ("{n} date", "{n} dates"),
        "times_unavailable": "<i>times unavailable</i>",
        "more_dates": ("<i>…and {n} more date on the website</i>",
                       "<i>…and {n} more dates on the website</i>"),
        "duration_min": "{n} min",
        "less_than_minute": "less than a minute",
        "status_title": "🤖 <b>Bot Status</b>",
        "status_subscribed": "Subscribed: {value}",
        "status_total": "Total subscribers: {n}",
        "status_last_check": "Last check: {value}",
        "status_next_check": "Next check: {value}",
        "yes": "✅ Yes",
        "no": "❌ No",
        "ago": "{duration} ago — {result}",
        "not_yet": "not yet",
        "in_about": "in ~{duration}",
        "unknown": "unknown",
        "result_found": "✅ slots found ({dates})",
        "result_none": "no slots",
        "result_timeout": "⚠️ request timed out",
        "result_error": "⚠️ error",
        "choose_language": "🌐 Choose your language:",
        "language_set": "✅ Language set to English.",
    },
    "pl": {
        "cmd_start": "Włącz powiadomienia",
        "cmd_check": "Sprawdź dostępność teraz",
        "cmd_status": "Status bota i czas następnego sprawdzenia",
        "cmd_stop": "Wyłącz powiadomienia",
        "cmd_language": "Zmień język",
        "btn_open_site": "📅 Otwórz stronę rezerwacji",
        "btn_check_again": "🔄 Sprawdź ponownie",
        "welcome": (
            "👋 Witaj w bocie monitorującym rezerwacje w Gdańsku!\n\n"
            "Powiadomię Cię, gdy pojawią się nowe wolne terminy.\n\n"
            "Komendy (również pod przyciskiem Menu):\n"
            "/start - Włącz powiadomienia\n"
            "/stop - Wyłącz powiadomienia\n"
            "/check - Sprawdź dostępność teraz\n"
            "/status - Status bota\n"
            "/language - Zmień język"
        ),
        "unsubscribed": "Wypisano Cię z powiadomień.",
        "not_subscribed": "Nie masz włączonych powiadomień.",
        "checking": "🔍 Sprawdzam dostępność...",
        "check_error": "❌ Błąd podczas sprawdzania dostępności: {error}",
        "checked_at": "<i>Sprawdzono o: {time}</i>",
        "slots_available": "✅ <b>Są wolne terminy!</b>",
        "no_slots": "❌ W tej chwili brak wolnych terminów.",
        "alert_title": "🎉 <b>Pojawiły się wolne terminy!</b>",
        "alert_body": "W Pomorskim Urzędzie Wojewódzkim w Gdańsku są dostępne nowe terminy.",
        "found_at": "<i>Znaleziono: {time}</i>",
        "slots_count": ("{n} termin", "{n} terminy", "{n} terminów"),
        "dates_count": ("{n} data", "{n} daty", "{n} dat"),
        "times_unavailable": "<i>godziny niedostępne</i>",
        "more_dates": ("<i>…i jeszcze {n} data na stronie</i>",
                       "<i>…i jeszcze {n} daty na stronie</i>",
                       "<i>…i jeszcze {n} dat na stronie</i>"),
        "duration_min": "{n} min",
        "less_than_minute": "mniej niż minutę",
        "status_title": "🤖 <b>Status bota</b>",
        "status_subscribed": "Powiadomienia: {value}",
        "status_total": "Liczba subskrybentów: {n}",
        "status_last_check": "Ostatnie sprawdzenie: {value}",
        "status_next_check": "Następne sprawdzenie: {value}",
        "yes": "✅ Tak",
        "no": "❌ Nie",
        "ago": "{duration} temu — {result}",
        "not_yet": "jeszcze nie było",
        "in_about": "za ~{duration}",
        "unknown": "nieznane",
        "result_found": "✅ znaleziono terminy ({dates})",
        "result_none": "brak terminów",
        "result_timeout": "⚠️ przekroczono czas oczekiwania",
        "result_error": "⚠️ błąd",
        "choose_language": "🌐 Wybierz język:",
        "language_set": "✅ Ustawiono język polski.",
    },
    "ru": {
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
    },
    "uk": {
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
    },
    "be": {
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
    },
}
