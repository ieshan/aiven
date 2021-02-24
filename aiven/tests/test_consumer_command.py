from dataclasses import dataclass, field
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

from aiven.commands.consumer import command as consumer_command

from .utils import MockThreadPoolExecutor


@dataclass
class EventItem():
	value: field(default_factory=list)


class ConsumerCommandTests(TestCase):
	@patch("aiven.commands.consumer.event_consumer")
	@patch("aiven.commands.consumer.EventStoreService")
	@patch("aiven.commands.consumer.ThreadPoolExecutor")
	def test_consumer_command(self, executor, store_service, event_consumer):
		executor.side_effect = MockThreadPoolExecutor
		event_item = EventItem(value={
			"url": "https://domain.tld",
			"http_status": 200,
			"timeout": False,
			"regex_matched": True,
			"event_time": datetime.now().isoformat(),
		})
		event_consumer.return_value.__iter__.return_value = [event_item,]
		store_service.return_value.loop.return_value = True

		runner = CliRunner()
		result = runner.invoke(consumer_command, catch_exceptions=True)

		self.assertEqual(result.exit_code, 0)
		store_service.return_value.add_event.assert_called_once_with(event_item.value)
		store_service.return_value.loop.assert_called_once()
