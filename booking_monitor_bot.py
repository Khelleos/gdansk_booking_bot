import asyncio
import html
import logging
import ssl
import random
import os
from datetime import datetime
import aiohttp
from dotenv import load_dotenv
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
from subscribers import (
    load_subscribers,
    add_subscriber,
    remove_subscriber,
    is_subscriber,
    get_subscribers,
    get_subscriber_count
)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
CHECK_INTERVAL = random.randint(600, 900)
API_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569/dates;servicePublicId=2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0;customSlotLength=40"
BOOKING_SITE_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/"
# Telegram rejects messages over 4096 characters; leave room for the header and footer
MAX_SLOTS_TEXT_LENGTH = 3500

BOT_COMMANDS = [
    BotCommand("start", "Start receiving notifications"),
    BotCommand("check", "Check availability now"),
    BotCommand("status", "Bot status and next check time"),
    BotCommand("stop", "Stop receiving notifications"),
]

OPEN_SITE_BUTTON = InlineKeyboardButton("📅 Open booking site", url=BOOKING_SITE_URL)
CHECK_AGAIN_BUTTON = InlineKeyboardButton("🔄 Check again", callback_data="check")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# httpx logs request URLs at INFO, and Telegram API URLs contain the bot token
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot_instance = None
check_task = None

# State of the background loop, shown by /status
last_check_at = None
last_check_result = None
next_check_at = None


async def fetch_times_for_date(session, date: str):
    """Fetch available times for a specific date."""
    try:
        times_url = f"https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569/dates/{date}/times;servicePublicId=2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0;customSlotLength=40"
        async with session.get(times_url, timeout=10) as response:
            if response.status == 200:
                return await response.json()
    except Exception as e:
        logger.warning(f"Error fetching times for date {date}: {e}")
    return []


async def fetch_slots():
    """Return {date: [times]} for every available date; empty dict if there are none.

    Raises on network errors and non-200 responses.
    """
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(API_URL, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(f"API returned status code {response.status}")
            data = await response.json()

        slots = {}
        if isinstance(data, list):
            for item in data:
                date = item.get('date')
                if date:
                    times = await fetch_times_for_date(session, date)
                    slots[date] = [t.get('time') for t in times if t.get('time')]
        return slots


def format_date(date: str) -> str:
    try:
        d = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return date
    return f"{d:%a}, {d.day} {d:%b %Y}"


def format_slots(slots: dict) -> str:
    """Render slots as HTML: one bold date per block, times in a collapsed blockquote."""
    parts = []
    length = 0
    for i, (date, times) in enumerate(slots.items()):
        if times:
            times_text = "\n".join(html.escape(t) for t in times)
            part = (
                f"<b>{html.escape(format_date(date))}</b> · {len(times)} slot{'s' if len(times) != 1 else ''}\n"
                f"<blockquote expandable>{times_text}</blockquote>"
            )
        else:
            part = f"<b>{html.escape(format_date(date))}</b>\n<i>times unavailable</i>"
        if length + len(part) > MAX_SLOTS_TEXT_LENGTH:
            parts.append(f"<i>…and {len(slots) - i} more dates on the website</i>")
            break
        parts.append(part)
        length += len(part)
    return "\n\n".join(parts)


def format_duration(seconds: float) -> str:
    minutes = round(seconds / 60)
    if minutes < 1:
        return "less than a minute"
    return f"{minutes} min"


async def check_availability_loop():
    global next_check_at
    next_check_at = datetime.now().timestamp() + 10
    await asyncio.sleep(10)
    logger.info("Starting availability check loop...")

    while True:
        try:
            await check_availability()
            next_check_at = datetime.now().timestamp() + CHECK_INTERVAL
            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Error in check loop: {e}")
            next_check_at = datetime.now().timestamp() + 60
            await asyncio.sleep(60)


async def check_availability():
    global CHECK_INTERVAL, last_check_at, last_check_result

    last_check_at = datetime.now()
    try:
        slots = await fetch_slots()
        if slots:
            logger.info(f"Availability found! Slots: {slots}")
            last_check_result = f"✅ slots found ({len(slots)} dates)"

            message = (
                "🎉 <b>Booking Availability Alert!</b>\n\n"
                "New appointments are available at Gdansk office.\n\n"
                f"{format_slots(slots)}\n\n"
                f"<i>Found at: {last_check_at.strftime('%Y-%m-%d %H:%M:%S')}</i>"
            )
            for chat_id in list(get_subscribers()):
                try:
                    await bot_instance.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode='HTML',
                        reply_markup=InlineKeyboardMarkup([[OPEN_SITE_BUTTON]])
                    )
                except Exception as e:
                    logger.error(f"Error sending message to {chat_id}: {e}")
                    if "Forbidden" in str(e) or "blocked" in str(e).lower():
                        remove_subscriber(chat_id)
        else:
            logger.info("No availability found (empty response)")
            last_check_result = "no slots"
    except asyncio.TimeoutError:
        logger.error("Request timeout while checking availability")
        last_check_result = "⚠️ request timed out"
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        last_check_result = "⚠️ error"

    CHECK_INTERVAL = random.randint(600, 900)
    logger.info(f"Updated check interval to {CHECK_INTERVAL} seconds ({CHECK_INTERVAL/60:.1f} minutes)")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_subscriber(chat_id)

    await update.message.reply_text(
        "👋 Welcome to the Gdansk Booking Monitor Bot!\n\n"
        "I will notify you when new appointment slots become available.\n\n"
        "Commands (also in the Menu button):\n"
        "/start - Start receiving notifications\n"
        "/stop - Stop receiving notifications\n"
        "/check - Manually check availability now\n"
        "/status - Check bot status"
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if remove_subscriber(chat_id):
        await update.message.reply_text("You have been unsubscribed from notifications.")
    else:
        await update.message.reply_text("You are not currently subscribed.")


async def show_check_result(message):
    """Run a manual check and edit `message` to show the result."""
    try:
        slots = await fetch_slots()
    except Exception as e:
        logger.error(f"Error in manual check: {e}")
        await message.edit_text(
            f"❌ Error checking availability: {html.escape(str(e) or type(e).__name__)}",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[CHECK_AGAIN_BUTTON]])
        )
        return

    checked_at = f"<i>Checked at: {datetime.now().strftime('%H:%M:%S')}</i>"
    if slots:
        text = f"✅ <b>Appointments are available!</b>\n\n{format_slots(slots)}\n\n{checked_at}"
        keyboard = [[OPEN_SITE_BUTTON], [CHECK_AGAIN_BUTTON]]
    else:
        text = f"❌ No appointments available at the moment.\n\n{checked_at}"
        keyboard = [[CHECK_AGAIN_BUTTON]]
    await message.edit_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))


async def check_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("🔍 Checking availability...")
    await show_check_result(message)


async def check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message = await query.edit_message_text("🔍 Checking availability...")
    await show_check_result(message)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    is_subscribed = is_subscriber(chat_id)
    now = datetime.now()

    if last_check_at:
        last_check = f"{format_duration((now - last_check_at).total_seconds())} ago — {last_check_result}"
    else:
        last_check = "not yet"
    if next_check_at:
        next_check = f"in ~{format_duration(max(0, next_check_at - now.timestamp()))}"
    else:
        next_check = "unknown"

    status_text = (
        f"🤖 <b>Bot Status</b>\n\n"
        f"Subscribed: {'✅ Yes' if is_subscribed else '❌ No'}\n"
        f"Total subscribers: {get_subscriber_count()}\n"
        f"Last check: {last_check}\n"
        f"Next check: {next_check}"
    )

    await update.message.reply_text(status_text, parse_mode='HTML')


async def post_init(application: Application):
    global bot_instance, check_task
    bot_instance = application.bot

    await application.bot.set_my_commands(BOT_COMMANDS)
    load_subscribers()

    check_task = asyncio.create_task(check_availability_loop())
    logger.info(f"Started availability checking loop (interval: {CHECK_INTERVAL} seconds)")


def main():
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("check", check_now))
    application.add_handler(CallbackQueryHandler(check_again, pattern="^check$"))
    application.add_handler(CommandHandler("status", status))

    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
