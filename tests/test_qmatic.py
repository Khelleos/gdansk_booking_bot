import unittest

from bot import config
from bot.qmatic import QmaticClient

SCHEDULE = (
    "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking/rest/schedule/branches/"
    "1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569"
)
PARAMS = "servicePublicId=2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0;customSlotLength=40"


class QmaticClientTest(unittest.TestCase):
    def test_urls(self):
        client = QmaticClient(
            config.BOOKING_BASE_URL, config.BRANCH_ID, config.SERVICE_ID, config.SLOT_LENGTH, config.REQUEST_TIMEOUT
        )
        self.assertEqual(client._url("dates"), f"{SCHEDULE}/dates;{PARAMS}")
        self.assertEqual(client._url("dates/2026-11-05/times"), f"{SCHEDULE}/dates/2026-11-05/times;{PARAMS}")
