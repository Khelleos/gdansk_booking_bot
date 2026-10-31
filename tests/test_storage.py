import json
import os
import tempfile
import unittest

from bot.storage import SubscriberStore


class SubscriberStoreTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "subscribers.json")

    def tearDown(self):
        self.dir.cleanup()

    def reload(self):
        store = SubscriberStore(self.path)
        store.load()
        return store

    def test_round_trip(self):
        store = self.reload()
        store.add(1, "pl")
        store.add(2, "be")
        self.assertTrue(store.set_language(1, "uk"))
        self.assertEqual(self.reload().get_all(), {1: "uk", 2: "be"})
        with open(self.path) as f:
            self.assertEqual(json.load(f), {"subscribers": [{"id": 1, "language": "uk"}, {"id": 2, "language": "be"}]})

    def test_old_format_loads_as_english(self):
        with open(self.path, "w") as f:
            json.dump({"subscribers": [1, 2]}, f)
        self.assertEqual(self.reload().get_all(), {1: "en", 2: "en"})

    def test_missing_file_is_empty(self):
        self.assertEqual(self.reload().count(), 0)

    def test_remove(self):
        store = self.reload()
        store.add(1, "en")
        self.assertTrue(store.remove(1))
        self.assertFalse(store.remove(1))
        self.assertFalse(self.reload().is_subscriber(1))

    def test_set_language_needs_a_subscriber(self):
        store = self.reload()
        self.assertFalse(store.set_language(1, "pl"))
        self.assertIsNone(store.get_language(1))

    def test_no_temporary_file_is_left(self):
        self.reload().add(1, "en")
        self.assertEqual(os.listdir(self.dir.name), ["subscribers.json"])
