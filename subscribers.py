import logging
import os
import json

from translations import DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)

SUBSCRIBERS_FILE = 'subscribers.json'

# chat_id -> language code
subscribers = {}


def load_subscribers():
    global subscribers
    try:
        if os.path.exists(SUBSCRIBERS_FILE):
            with open(SUBSCRIBERS_FILE, 'r') as f:
                data = json.load(f)
            subscribers = {}
            for entry in data.get('subscribers', []):
                # Older files stored bare chat IDs
                if isinstance(entry, dict):
                    subscribers[entry['id']] = entry.get('language') or DEFAULT_LANGUAGE
                else:
                    subscribers[entry] = DEFAULT_LANGUAGE
            logger.info(f"Loaded {len(subscribers)} subscribers from file")
        else:
            logger.info("No existing subscribers file found")
            subscribers = {}
    except Exception as e:
        logger.error(f"Error loading subscribers: {e}")
        subscribers = {}


def _save_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(
                {'subscribers': [{'id': chat_id, 'language': lang} for chat_id, lang in subscribers.items()]},
                f
            )
        logger.info(f"Saved {len(subscribers)} subscribers to file")
    except Exception as e:
        logger.error(f"Error saving subscribers: {e}")


def add_subscriber(chat_id, language):
    subscribers[chat_id] = language
    _save_subscribers()
    logger.info(f"New subscriber: {chat_id} ({language}, Total: {len(subscribers)})")


def remove_subscriber(chat_id):
    if chat_id in subscribers:
        del subscribers[chat_id]
        _save_subscribers()
        logger.info(f"Subscriber removed: {chat_id} (Total: {len(subscribers)})")
        return True
    return False


def is_subscriber(chat_id):
    return chat_id in subscribers


def get_language(chat_id):
    """Saved language of a subscriber, or None if the chat isn't subscribed."""
    return subscribers.get(chat_id)


def set_language(chat_id, language):
    """Save the language of a subscriber; returns False if the chat isn't subscribed."""
    if chat_id not in subscribers:
        return False
    subscribers[chat_id] = language
    _save_subscribers()
    return True


def get_subscribers():
    """Return {chat_id: language} for every subscriber."""
    return dict(subscribers)


def get_subscriber_count():
    return len(subscribers)
