import json
import threading
import time

from typing import Callable

import psycopg2.extras
from kafka import KafkaConsumer, KafkaProducer

import aiven.config as config
from aiven.db import get_connection


def event_consumer(topic, client_id, group_id):
	return KafkaConsumer(
		topic,
		auto_offset_reset="earliest",
		bootstrap_servers=config.KAFKA_HOST,
		client_id=client_id,
		enable_auto_commit=False,
		group_id=group_id,
		security_protocol="SSL",
		ssl_cafile=config.KAFKA_CA_FILE,
		ssl_certfile=config.KAFKA_CERT_FILE,
		ssl_keyfile=config.KAFKA_KEY_FILE,
		value_deserializer=lambda m: json.loads(m.decode("ascii")),
	)


def event_producer():
	return KafkaProducer(
		bootstrap_servers=config.KAFKA_HOST,
		security_protocol="SSL",
		ssl_cafile=config.KAFKA_CA_FILE,
		ssl_certfile=config.KAFKA_CERT_FILE,
		ssl_keyfile=config.KAFKA_KEY_FILE,
		value_serializer=lambda m: json.dumps(m).encode("ascii"),
	)


class EventStoreService:
	_events = []
	_lock = threading.Lock()
	_loop_keep_alive = True
	_loop_ended = False

	def __init__(self):
		self._conn = get_connection()

	def add_event(self, event):
		with self._lock:
			self._events.append(event)

	def save_events(self):
		with self._lock:
			if not self._events:
				return False

			# For bulk insert approaches: https://hakibenita.com/fast-load-data-python-postgresql
			with self._conn.cursor() as cursor:
				psycopg2.extras.execute_values(
					cursor,
					'INSERT INTO server_status ("url", "timeout", "http_status", "regex_matched", "event_time") VALUES %s',
					(
						(
							event["url"],
							event["timeout"],
							event["http_status"],
							event["regex_matched"],
							event["event_time"],
						) for event in self._events),
					page_size=1000
				)
				del self._events[:]
		return True

	def kill_loop(self):
		self._loop_keep_alive = False
		while not self._loop_ended:
			time.sleep(0.1)

	def loop(self, frequency:int=30, callback:Callable=None):
		while self._loop_keep_alive:
			self.save_events()
			if callback:
				callback()
			time.sleep(frequency)
		self._loop_ended = True
