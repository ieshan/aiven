import re

from datetime import datetime
from typing import Tuple, Union

import requests


def get_http_status(url: str, timeout: int) -> int:
	res = requests.head(url, timeout=timeout)
	return res.status_code


def get_http_body(url: str, timeout: int) -> Tuple[int, str]:
	res = requests.get(url, timeout=timeout)
	return res.status_code, res.text


def get_server_status_message(url: str, timeout: int, regex: Union[None, str]=None) -> dict:
	data = {
		"url": url,
		"http_status": None,
		"timeout": False,
		"regex_matched": None,
		"event_time": datetime.now().isoformat(),
	}
	try:
		if not regex:
			data["http_status"] = get_http_status(url, timeout)
		else:
			data["http_status"], body = get_http_body(url, timeout)
			data["regex_matched"] = bool(re.search(regex, body))
	except requests.exceptions.Timeout:
		data["timeout"] = True

	return data
