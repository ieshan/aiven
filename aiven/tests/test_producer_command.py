from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

import aiven.config as config
from aiven.commands.producer import command as producer_command


class ProducerCommandTests(TestCase):
	@patch("time.sleep")
	@patch("aiven.commands.producer.event_producer")
	@patch("aiven.commands.producer.get_server_status_message")
	def test_producer_command(self, get_server_status_msg, event_producer, sleep):
		status_msg = {
			"url": "https://domain.tld",
			"http_status": 200,
			"timeout": False,
			"regex_matched": True,
			"event_time": datetime.now().isoformat(),
		}
		get_server_status_msg.return_value = status_msg

		class SleepException(Exception):
			pass

		sleep.side_effect = SleepException

		runner = CliRunner()
		result = runner.invoke(producer_command, ["-u", status_msg["url"], ])

		self.assertIsInstance(result.exception, SleepException)
		event_producer.return_value.send.assert_called_once()
		event_producer.return_value.send.assert_called_with(config.KAFKA_TOPIC, status_msg)
