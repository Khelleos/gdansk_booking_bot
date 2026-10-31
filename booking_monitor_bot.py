import asyncio
import logging
import ssl
import random
import os
from datetime import datetime
import aiohttp
from dotenv import load_dotenv
from telegram import BotCommand, BotCommandScopeChat, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import messages
from subscribers import (
    load_subscribers,
    add_subscriber,
    remove_subscriber,
    is_subscriber,
    get_language,
    set_language,
    get_subscribers,
    get_subscriber_count
)
from translations import DEFAULT_LANGUAGE, LANGUAGES

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
CHECK_INTERVAL = random.randint(600, 900)
API_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569/dates;servicePublicId=2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0;customSlotLength=40"
BOOKING_SITE_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/"

LANGUAGE_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton(name, callback_data=f"lang:{code}")] for code, name in LANGUAGES.items()]
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# httpx logs request URLs at INFO, and Telegram API URLs contain the bot token
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot_instance = None
check_task = None

# State of the background loop, shown by /status.
# last_check_result is a (result, dates) pair for messages.check_result_label
last_check_at = None
last_check_result = None
next_check_at = None


def bot_commands(lang):
    return [BotCommand(command, description) for command, description in messages.command_descriptions(lang)]


def open_site_button(lang):
    return InlineKeyboardButton(messages.open_site_button(lang), url=BOOKING_SITE_URL)


def check_again_button(lang):
    return InlineKeyboardButton(messages.check_again_button(lang), callback_data="check")


def chat_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Saved subscriber language, then a choice made while unsubscribed, then the Telegram app language."""
    lang = get_language(update.effective_chat.id) or context.chat_data.get('language')
    if lang:
        return lang
    user = update.effective_user
    return messages.detect_language(user.language_code if user else None)


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
            last_check_result = ("found", len(slots))

            # Render each language once, not once per subscriber
            alerts = {}
            for chat_id, lang in get_subscribers().items():
                if lang not in alerts:
                    alerts[lang] = messages.availability_alert(lang, slots, last_check_at)
                try:
                    await bot_instance.send_message(
                        chat_id=chat_id,
                        text=alerts[lang],
                        parse_mode='HTML',
                        reply_markup=InlineKeyboardMarkup([[open_site_button(lang)]])
                    )
                except Exception as e:
                    logger.error(f"Error sending message to {chat_id}: {e}")
                    if "Forbidden" in str(e) or "blocked" in str(e).lower():
                        remove_subscriber(chat_id)
        else:
            logger.info("No availability found (empty response)")
            last_check_result = ("none", 0)
    except asyncio.TimeoutError:
        logger.error("Request timeout while checking availability")
        last_check_result = ("timeout", 0)
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        last_check_result = ("error", 0)

    CHECK_INTERVAL = random.randint(600, 900)
    logger.info(f"Updated check interval to {CHECK_INTERVAL} seconds ({CHECK_INTERVAL/60:.1f} minutes)")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = chat_language(update, context)
    add_subscriber(chat_id, lang)
    await update.message.reply_text(messages.welcome(lang))


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = chat_language(update, context)
    # Remember the language until restart in case the chat subscribes again
    context.chat_data['language'] = lang
    if remove_subscriber(chat_id):
        await update.message.reply_text(messages.unsubscribed(lang))
    else:
        await update.message.reply_text(messages.not_subscribed(lang))


async def show_check_result(message, lang):
    """Run a manual check and edit `message` to show the result."""
    try:
        slots = await fetch_slots()
    except Exception as e:
        logger.error(f"Error in manual check: {e}")
        await message.edit_text(
            messages.check_error(lang, str(e) or type(e).__name__),
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[check_again_button(lang)]])
        )
        return

    if slots:
        keyboard = [[open_site_button(lang)], [check_again_button(lang)]]
    else:
        keyboard = [[check_again_button(lang)]]
    await message.edit_text(
        messages.check_result(lang, slots, datetime.now()),
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def check_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = chat_language(update, context)
    message = await update.message.reply_text(messages.checking(lang))
    await show_check_result(message, lang)


async def check_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = chat_language(update, context)
    message = await query.edit_message_text(messages.checking(lang))
    await show_check_result(message, lang)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = chat_language(update, context)
    status_text = messages.status(
        lang,
        is_subscribed=is_subscriber(chat_id),
        total=get_subscriber_count(),
        last_check_at=last_check_at,
        last_result=last_check_result,
        next_check_at=next_check_at,
        now=datetime.now(),
    )
    await update.message.reply_text(status_text, parse_mode='HTML')


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = chat_language(update, context)
    await update.message.reply_text(messages.choose_language(lang), reply_markup=LANGUAGE_KEYBOARD)


async def language_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split(':', 1)[1]
    if lang not in LANGUAGES:
        return
    chat_id = update.effective_chat.id
    set_language(chat_id, lang)
    context.chat_data['language'] = lang
    # Show this chat's menu in the chosen language instead of the Telegram app language
    await context.bot.set_my_commands(bot_commands(lang), scope=BotCommandScopeChat(chat_id))
    await query.edit_message_text(messages.language_set(lang))


async def post_init(application: Application):
    global bot_instance, check_task
    bot_instance = application.bot

    # The default menu is English; Telegram shows the others by the user's app language
    await application.bot.set_my_commands(bot_commands(DEFAULT_LANGUAGE))
    for lang in LANGUAGES:
        if lang != DEFAULT_LANGUAGE:
            await application.bot.set_my_commands(bot_commands(lang), language_code=lang)
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
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CallbackQueryHandler(language_chosen, pattern="^lang:"))

    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
