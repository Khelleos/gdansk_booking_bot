"""
Module for managing booking notification subscribers.
Handles loading, saving, and managing subscriber list.
"""

import logging
import os
import json

# Set up logging
logger = logging.getLogger(__name__)

# Persistence file for subscribers
SUBSCRIBERS_FILE = 'subscribers.json'

# Store chat IDs of users who want notifications
subscribers = set()


def load_subscribers():
    """Load subscribers from JSON file."""
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


def save_subscribers():
    """Save subscribers to JSON file."""
    try:
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump({'subscribers': list(subscribers)}, f)
        logger.info(f"Saved {len(subscribers)} subscribers to file")
    except Exception as e:
        logger.error(f"Error saving subscribers: {e}")


def add_subscriber(chat_id):
    """Add a subscriber to the list."""
    subscribers.add(chat_id)
    save_subscribers()
    logger.info(f"New subscriber: {chat_id} (Total: {len(subscribers)})")


def remove_subscriber(chat_id):
    """Remove a subscriber from the list."""
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers()
        logger.info(f"Subscriber removed: {chat_id} (Total: {len(subscribers)})")
        return True
    return False


def is_subscriber(chat_id):
    """Check if a chat ID is in the subscribers list."""
    return chat_id in subscribers


def get_subscribers():
    """Get the list of all subscribers."""
    return list(subscribers)


def get_subscriber_count():
    """Get the total number of subscribers."""
    return len(subscribers)


def remove_blocked_subscriber(chat_id):
    """Remove a subscriber who has blocked the bot."""
    subscribers.discard(chat_id)
    save_subscribers()
    logger.info(f"Removed blocked subscriber: {chat_id}")
