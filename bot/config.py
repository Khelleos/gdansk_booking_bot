import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Qmatic web booking of the Gdansk voivodeship office. The branch is the office,
# the service is the appointment type
BOOKING_BASE_URL = "https://rezerwacja.gdansk.uw.gov.pl:8445/qmaticwebbooking"
BOOKING_SITE_URL = f"{BOOKING_BASE_URL}/"
BRANCH_ID = "1cf1e3e60eeb96dae2bb572487249bd48cc5bed0024960eaee0c893ce4918569"
SERVICE_ID = "2c5251d564aaf0b09c2a39d69cf7ed4cb1e142ab3a501b4b688e1e7c2d80b8e0"
SLOT_LENGTH = 40
REQUEST_TIMEOUT = 10

# Background checks wait a random number of seconds in this range, so polling isn't regular
CHECK_INTERVAL_RANGE = (600, 900)
FIRST_CHECK_DELAY = 10
RETRY_DELAY = 60


@dataclass(frozen=True)
class Config:
    telegram_bot_token: str
    subscribers_file: Path


def load() -> Config:
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
    return Config(
        telegram_bot_token=token,
        subscribers_file=Path('subscribers.json'),
    )
