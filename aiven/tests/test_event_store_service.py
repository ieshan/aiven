from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from aiven.service import EventStoreService


class EventStoreServiceTests(TestCase):
	@patch("aiven.service.get_connection")
	def test_save_events_should_return_false_if_no_events_to_save(self, connection):
		event_store = EventStoreService()
		result = event_store.save_events()
		self.assertEqual(result, False)

	@patch("aiven.service.get_connection")
	@patch("aiven.service.psycopg2.extras.execute_values")
	def test_save_events_return_true_if_event_stored(self, connection, execute_values):
		event_store = EventStoreService()
		event_store.add_event({
			"url": "https://domain.tld",
			"http_status": 200,
			"timeout": False,
			"regex_matched": True,
			"event_time": datetime.now().isoformat(),
		})
		result = event_store.save_events()
		self.assertEqual(result, True)
		execute_values.assert_called_once()
