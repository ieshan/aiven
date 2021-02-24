import logging
import signal
import time

import click

import aiven.config as config
from aiven.service import event_producer
from aiven.utils import get_server_status_message


logger = logging.getLogger(__name__)


@click.command(name="producer")
@click.option("--url", "-u", type=str, required=True)
@click.option("--interval", "-i", type=int, default=30, show_default=True)
@click.option("--timeout", "-t", type=int, default=3, show_default=True)
@click.option("--regex", "-r", default=None, show_default=True)
def command(url, timeout, interval, regex):
	producer = event_producer()
	# Handle exit gracefully
	is_running = True
	def exit_handler(*args):
		nonlocal is_running
		is_running = False
		producer.flush()
		producer.close()
		logger.debug("Handled exit signal")

	signal.signal(signal.SIGINT, exit_handler)
	signal.signal(signal.SIGTERM, exit_handler)

	def on_send_error(exc):
		logger.error("kafka send error", exc_info=exc)

	while is_running:
		message = get_server_status_message(url, timeout, regex)
		producer.send(config.KAFKA_TOPIC, message).add_errback(on_send_error)
		logger.debug("Published event")
		time.sleep(interval)
