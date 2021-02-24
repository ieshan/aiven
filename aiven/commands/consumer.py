import logging
import signal
from concurrent.futures import ThreadPoolExecutor

import click

import aiven.config as config
from aiven.service import event_consumer, EventStoreService


keep_alive = True
logger = logging.getLogger(__name__)


@click.command()
@click.option("--frequency", "-f", type=int, default=5, show_default=True)
def command(frequency):
	consumer = event_consumer(
		topic=config.KAFKA_TOPIC,
		client_id=config.KAFKA_CLIENT_ID,
		group_id=config.KAFKA_GROUP_ID,
	)

	store_service = EventStoreService()

	def commit_consumer():
		consumer.commit()

	def consumer_loop():
		try:
			for msg in consumer:
				store_service.add_event(msg.value)
		except Exception as ex:
			logger.exception("consumer exception", exc_info=ex)

	# Handle exit gracefully
	def exit_handler(*args):
		store_service.kill_loop()
		store_service.save_events()
		consumer.commit()
		consumer.close()
	signal.signal(signal.SIGTERM, exit_handler)
	signal.signal(signal.SIGINT, exit_handler)

	# Guide on ThreadPoolExecutor usage: https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
	with ThreadPoolExecutor(max_workers=2) as executor:
		executor.submit(consumer_loop)
		executor.submit(store_service.loop, frequency, commit_consumer)
