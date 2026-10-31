import asyncio
import os
import tempfile
import unittest

from bot.monitor import Monitor
from bot.storage import SubscriberStore

SLOTS = {"2026-11-05": ["09:00"]}


class FakeClient:
    def __init__(self, result):
        self.result = result

    async def fetch_slots(self):
        if isinstance(self.result, BaseException):
            raise self.result
        return self.result


class FakeBot:
    def __init__(self, blocked=()):
        self.blocked = blocked
        self.sent = {}

    async def send_message(self, chat_id, text, **kwargs):
        if chat_id in self.blocked:
            raise Exception("Forbidden: bot was blocked by the user")
        self.sent[chat_id] = text


class MonitorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.store = SubscriberStore(os.path.join(self.dir.name, "subscribers.json"))
        self.store.add(1, "pl")
        self.store.add(2, "uk")
        self.store.add(3, "en")

    def tearDown(self):
        self.dir.cleanup()

    async def test_alerts_each_subscriber_in_their_language(self):
        bot = FakeBot()
        monitor = Monitor(bot, FakeClient(SLOTS), self.store)
        await monitor.check()
        self.assertIn("Pojawiły się wolne terminy", bot.sent[1])
        self.assertIn("З'явилися вільні місця", bot.sent[2])
        self.assertIn("Booking Availability Alert", bot.sent[3])
        self.assertEqual(monitor.last_result, ("found", 1))

    async def test_blocked_subscribers_are_removed(self):
        bot = FakeBot(blocked={3})
        await Monitor(bot, FakeClient(SLOTS), self.store).check()
        self.assertEqual(set(bot.sent), {1, 2})
        self.assertFalse(self.store.is_subscriber(3))

    async def test_results_without_slots(self):
        cases = [({}, ("none", 0)), (asyncio.TimeoutError(), ("timeout", 0)), (RuntimeError("500"), ("error", 0))]
        for result, expected in cases:
            with self.subTest(expected=expected):
                bot = FakeBot()
                monitor = Monitor(bot, FakeClient(result), self.store)
                await monitor.check()
                self.assertEqual(monitor.last_result, expected)
                self.assertEqual(bot.sent, {})
