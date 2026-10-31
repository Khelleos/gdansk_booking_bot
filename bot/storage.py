import logging
import os
import json

from bot.i18n.translations import DEFAULT_LANGUAGE

logger = logging.getLogger(__name__)


class SubscriberStore:
    """Subscribers and their languages, written to a JSON file on every change.

    The file looks like {"subscribers": [{"id": 123, "language": "pl"}]}.
    """

    def __init__(self, path):
        self.path = path
        # chat_id -> language code
        self._subscribers = {}

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    data = json.load(f)
                self._subscribers = {}
                for entry in data.get('subscribers', []):
                    # Older files stored bare chat IDs
                    if isinstance(entry, dict):
                        self._subscribers[entry['id']] = entry.get('language') or DEFAULT_LANGUAGE
                    else:
                        self._subscribers[entry] = DEFAULT_LANGUAGE
                logger.info(f"Loaded {len(self._subscribers)} subscribers from file")
            else:
                logger.info("No existing subscribers file found")
                self._subscribers = {}
        except Exception as e:
            logger.error(f"Error loading subscribers: {e}")
            self._subscribers = {}

    def _save(self):
        # Write a temporary file and swap it in, so a crash mid-write can't leave
        # a broken file that would load as no subscribers
        tmp_path = f"{self.path}.tmp"
        try:
            with open(tmp_path, 'w') as f:
                json.dump(
                    {'subscribers': [{'id': chat_id, 'language': lang}
                                     for chat_id, lang in self._subscribers.items()]},
                    f
                )
            os.replace(tmp_path, self.path)
            logger.info(f"Saved {len(self._subscribers)} subscribers to file")
        except Exception as e:
            logger.error(f"Error saving subscribers: {e}")

    def add(self, chat_id, language):
        self._subscribers[chat_id] = language
        self._save()
        logger.info(f"New subscriber: {chat_id} ({language}, Total: {len(self._subscribers)})")

    def remove(self, chat_id):
        if chat_id in self._subscribers:
            del self._subscribers[chat_id]
            self._save()
            logger.info(f"Subscriber removed: {chat_id} (Total: {len(self._subscribers)})")
            return True
        return False

    def is_subscriber(self, chat_id):
        return chat_id in self._subscribers

    def get_language(self, chat_id):
        """Saved language of a subscriber, or None if the chat isn't subscribed."""
        return self._subscribers.get(chat_id)

    def set_language(self, chat_id, language):
        """Save the language of a subscriber; returns False if the chat isn't subscribed."""
        if chat_id not in self._subscribers:
            return False
        self._subscribers[chat_id] = language
        self._save()
        return True

    def get_all(self):
        """Return {chat_id: language} for every subscriber."""
        return dict(self._subscribers)

    def count(self):
        return len(self._subscribers)
