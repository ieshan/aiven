import click

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

import aiven.config as config
from aiven.db import get_connection


@click.command(name="migrate")
def command():
	connection =get_connection()
	with connection.cursor() as cursor:
		cursor.execute("CREATE SEQUENCE IF NOT EXISTS server_status_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;")
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS "public"."server_status" (
			"id" integer DEFAULT nextval('server_status_id_seq') NOT NULL,
			"url" character varying(200) NOT NULL,
			"timeout" boolean,
			"http_status" smallint,
			"regex_matched" boolean,
			"event_time" timestamp NOT NULL,
			"created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
			CONSTRAINT "server_status_pkey" PRIMARY KEY ("id")
		) WITH (oids = false);
		""")

	kafka_admin = KafkaAdminClient(
		bootstrap_servers=config.KAFKA_HOST,
		client_id=config.KAFKA_CLIENT_ID,
		security_protocol="SSL",
		ssl_cafile=config.KAFKA_CA_FILE,
		ssl_certfile=config.KAFKA_CERT_FILE,
		ssl_keyfile=config.KAFKA_KEY_FILE,
	)
	topics = [
		NewTopic(name=config.KAFKA_TOPIC, num_partitions=1, replication_factor=1),
	]
	try:
		kafka_admin.create_topics(new_topics=topics, validate_only=False)
	except TopicAlreadyExistsError:
		pass

