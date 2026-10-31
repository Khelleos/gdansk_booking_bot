# Native name, shown in the /language picker
NAME = "Polski"

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = [
    "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia",
]

# Short weekday names, Monday first
WEEKDAYS = ["pon.", "wt.", "śr.", "czw.", "pt.", "sob.", "niedz."]

STRINGS = {
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
}
