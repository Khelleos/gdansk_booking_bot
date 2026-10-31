import logging

from telegram.ext import Application

from bot import config, handlers
from bot.i18n.translations import DEFAULT_LANGUAGE, LANGUAGES
from bot.keyboards import bot_commands
from bot.monitor import Monitor
from bot.qmatic import QmaticClient
from bot.storage import SubscriberStore

logger = logging.getLogger(__name__)


async def post_init(application: Application):
    # The default menu is English; Telegram shows the others by the user's app language
    await application.bot.set_my_commands(bot_commands(DEFAULT_LANGUAGE))
    for lang in LANGUAGES:
        if lang != DEFAULT_LANGUAGE:
            await application.bot.set_my_commands(bot_commands(lang), language_code=lang)

    store = application.bot_data['store']
    store.load()

    monitor = Monitor(application.bot, application.bot_data['client'], store)
    application.bot_data['monitor'] = monitor
    monitor.start()


async def post_shutdown(application: Application):
    # post_init may have failed before the monitor was created
    monitor = application.bot_data.get('monitor')
    if monitor is not None:
        await monitor.stop()
    await application.bot_data['client'].close()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # httpx logs request URLs at INFO, and Telegram API URLs contain the bot token
    logging.getLogger("httpx").setLevel(logging.WARNING)

    cfg = config.load()

    application = (
        Application.builder()
        .token(cfg.telegram_bot_token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    application.bot_data['store'] = SubscriberStore(cfg.subscribers_file)
    application.bot_data['client'] = QmaticClient(
        config.BOOKING_BASE_URL,
        config.BRANCH_ID,
        config.SERVICE_ID,
        config.SLOT_LENGTH,
        config.REQUEST_TIMEOUT,
    )
    handlers.register(application)

    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)
