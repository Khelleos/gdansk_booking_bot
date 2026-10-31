# Native name, shown in the /language picker
NAME = "English"

# Month names in the form used after a day number ("5 listopada"), January first
MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

# Short weekday names, Monday first
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

STRINGS = {
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
}
