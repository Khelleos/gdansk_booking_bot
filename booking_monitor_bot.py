"""
Telegram bot that monitors booking availability at Gdansk office.
Sends a notification when appointments become available.
"""

import asyncio
import logging
import ssl
from datetime import datetime
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration
TELEGRAM_BOT_TOKEN = "8559276274:AAEv9su-Io6YbMzsEdOJXOGdsSB6I9WGWzg"  # Replace with your bot token
CHECK_INTERVAL = 300  # Check every 5 minutes (in seconds)
API_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569/dates;servicePublicId=2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0;customSlotLength=40"

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store chat IDs of users who want notifications
subscribers = set()

# Global variable to store the bot instance
bot_instance = None
check_task = None


async def check_availability_loop():
    """Continuously check the booking API for availability."""
    await asyncio.sleep(10)  # Initial delay
    logger.info("Starting availability check loop...")
    
    while True:
        try:
            await check_availability()
            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            logger.error(f"Error in check loop: {e}")
            await asyncio.sleep(60)  # Wait a minute before retrying


async def check_availability():
    """Check the booking API for availability and notify subscribers."""
    try:
        # Create SSL context that doesn't verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(API_URL, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check if response has data (not empty)
                    if data:
                        logger.info(f"Availability found! Data: {data}")
                        
                        # Send notification to all subscribers
                        for chat_id in list(subscribers):
                            try:
                                message = (
                                    "🎉 <b>Booking Availability Alert!</b>\n\n"
                                    "New appointments are available at Gdansk office.\n\n"
                                    f"Check the website now: https://rezerwacja.gdansk.uw.gov.pl/\n\n"
                                    f"<i>Found at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
                                )
                                await bot_instance.send_message(
                                    chat_id=chat_id,
                                    text=message,
                                    parse_mode='HTML'
                                )
                            except Exception as e:
                                logger.error(f"Error sending message to {chat_id}: {e}")
                                if "Forbidden" in str(e) or "blocked" in str(e).lower():
                                    subscribers.discard(chat_id)
                                    logger.info(f"Removed blocked subscriber: {chat_id}")
                    else:
                        logger.info("No availability found (empty response)")
                else:
                    logger.warning(f"API returned status code: {response.status}")
                    
    except asyncio.TimeoutError:
        logger.error("Request timeout while checking availability")
    except Exception as e:
        logger.error(f"Error checking availability: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    
    await update.message.reply_text(
        "👋 Welcome to the Gdansk Booking Monitor Bot!\n\n"
        "I will notify you when new appointment slots become available.\n\n"
        "Commands:\n"
        "/start - Start receiving notifications\n"
        "/stop - Stop receiving notifications\n"
        "/check - Manually check availability now\n"
        "/status - Check bot status"
    )
    logger.info(f"New subscriber: {chat_id} (Total: {len(subscribers)})")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /stop command."""
    chat_id = update.effective_chat.id
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        await update.message.reply_text("You have been unsubscribed from notifications.")
        logger.info(f"Subscriber removed: {chat_id} (Total: {len(subscribers)})")
    else:
        await update.message.reply_text("You are not currently subscribed.")


async def check_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /check command - manually check availability."""
    await update.message.reply_text("Checking availability now...")
    
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(API_URL, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data:
                        await update.message.reply_text(
                            "✅ Appointments are available!\n"
                            "Check the website: https://rezerwacja.gdansk.uw.gov.pl/"
                        )
                    else:
                        await update.message.reply_text(
                            "❌ No appointments available at the moment."
                        )
                else:
                    await update.message.reply_text(
                        f"⚠️ Error: API returned status code {response.status}"
                    )
    except Exception as e:
        await update.message.reply_text(f"❌ Error checking availability: {str(e)}")
        logger.error(f"Error in manual check: {e}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /status command."""
    chat_id = update.effective_chat.id
    is_subscribed = chat_id in subscribers
    
    status_text = (
        f"🤖 <b>Bot Status</b>\n\n"
        f"Subscribed: {'✅ Yes' if is_subscribed else '❌ No'}\n"
        f"Total subscribers: {len(subscribers)}\n"
        f"Check interval: {CHECK_INTERVAL} seconds\n"
        f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    await update.message.reply_text(status_text, parse_mode='HTML')


async def post_init(application: Application):
    """Initialize after the application starts."""
    global bot_instance, check_task
    bot_instance = application.bot
    
    # Start the background check loop
    check_task = asyncio.create_task(check_availability_loop())
    logger.info(f"Started availability checking loop (interval: {CHECK_INTERVAL} seconds)")


def main():
    """Start the bot."""
    # Create the Application
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("check", check_now))
    application.add_handler(CommandHandler("status", status))

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()