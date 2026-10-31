import asyncio
import logging
import random
from datetime import datetime

from telegram import InlineKeyboardMarkup

from bot.config import CHECK_INTERVAL_RANGE, FIRST_CHECK_DELAY, RETRY_DELAY
from bot.i18n import messages
from bot.keyboards import open_site_button

logger = logging.getLogger(__name__)


class Monitor:
    """Polls the booking API in the background and alerts subscribers when slots appear.

    Its last-check state is what /status shows; manual checks don't change it.
    """

    def __init__(self, bot, client, store):
        self.bot = bot
        self.client = client
        self.store = store
        self.interval = random.randint(*CHECK_INTERVAL_RANGE)
        self.last_check_at = None
        # (result, dates) pair for messages.check_result_label
        self.last_result = None
        self.next_check_at = None
        self._task = None

    def start(self):
        self._task = asyncio.create_task(self._run())
        logger.info(f"Started availability checking loop (interval: {self.interval} seconds)")

    async def stop(self):
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run(self):
        self.next_check_at = datetime.now().timestamp() + FIRST_CHECK_DELAY
        await asyncio.sleep(FIRST_CHECK_DELAY)
        logger.info("Starting availability check loop...")

        while True:
            try:
                await self.check()
                self.next_check_at = datetime.now().timestamp() + self.interval
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in check loop: {e}")
                self.next_check_at = datetime.now().timestamp() + RETRY_DELAY
                await asyncio.sleep(RETRY_DELAY)

    async def check(self):
        """Check once, alert every subscriber if there are slots, and pick the next interval."""
        self.last_check_at = datetime.now()
        try:
            slots = await self.client.fetch_slots()
            if slots:
                logger.info(f"Availability found! Slots: {slots}")
                self.last_result = ("found", len(slots))
                await self._broadcast(slots)
            else:
                logger.info("No availability found (empty response)")
                self.last_result = ("none", 0)
        except asyncio.TimeoutError:
            logger.error("Request timeout while checking availability")
            self.last_result = ("timeout", 0)
        except Exception as e:
            logger.error(f"Error checking availability: {e}")
            self.last_result = ("error", 0)

        self.interval = random.randint(*CHECK_INTERVAL_RANGE)
        logger.info(f"Updated check interval to {self.interval} seconds ({self.interval/60:.1f} minutes)")

    async def _broadcast(self, slots: dict):
        # Render each language once, not once per subscriber
        alerts = {}
        for chat_id, lang in self.store.get_all().items():
            if lang not in alerts:
                alerts[lang] = messages.availability_alert(lang, slots, self.last_check_at)
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=alerts[lang],
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup([[open_site_button(lang)]])
                )
            except Exception as e:
                logger.error(f"Error sending message to {chat_id}: {e}")
                if "Forbidden" in str(e) or "blocked" in str(e).lower():
                    self.store.remove(chat_id)
