import logging
import os
import json

logger = logging.getLogger(__name__)

SUBSCRIBERS_FILE = 'subscribers.json'

subscribers = set()


def load_subscribers():
    global subscribers
    try:
        if os.path.exists(SUBSCRIBERS_FILE):
            with open(SUBSCRIBERS_FILE, 'r') as f:
                data = json.load(f)
                subscribers = set(data.get('subscribers', []))
                logger.info(f"Loaded {len(subscribers)} subscribers from file")
        else:
            logger.info("No existing subscribers file found")
            subscribers = set()
    except Exception as e:
        logger.error(f"Error loading subscribers: {e}")
        subscribers = set()


def _save_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump({'subscribers': list(subscribers)}, f)
        logger.info(f"Saved {len(subscribers)} subscribers to file")
    except Exception as e:
        logger.error(f"Error saving subscribers: {e}")


def add_subscriber(chat_id):
    subscribers.add(chat_id)
    _save_subscribers()
    logger.info(f"New subscriber: {chat_id} (Total: {len(subscribers)})")


def remove_subscriber(chat_id):
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        _save_subscribers()
        logger.info(f"Subscriber removed: {chat_id} (Total: {len(subscribers)})")
        return True
    return False


def is_subscriber(chat_id):
    return chat_id in subscribers


def get_subscribers():
    return list(subscribers)


def get_subscriber_count():
    return len(subscribers)
