from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import Timeout

from aiven.utils import get_server_status_message


class UtilsTests(TestCase):
	@patch("aiven.utils.get_http_status")
	def test_get_server_status_message_with_timeout(self, get_http_status):
		get_http_status.side_effect = Timeout

		message = get_server_status_message("https://domain.tld", timeout=1)
		self.assertEqual(message["timeout"], True)

	@patch("aiven.utils.get_http_body")
	def test_get_server_status_message_regex_not_match(self, get_http_body):
		get_http_body.return_value = (200, "Not Ok")

		message = get_server_status_message("https://domain.tld", timeout=1, regex="^Ok")
		self.assertEqual(message["regex_matched"], False)

	@patch("aiven.utils.get_http_body")
	def test_get_server_status_message_regex_match(self, get_http_body):
		get_http_body.return_value = (200, "Ok")

		message = get_server_status_message("https://domain.tld", timeout=1, regex="^Ok$")
		self.assertEqual(message["regex_matched"], True)
