import psycopg2
import aiven.config as config


_connection = None


def get_connection():
	global _connection
	if not _connection:
		_connection = psycopg2.connect(config.DATABASE_URL)
		_connection.autocommit = True
	return _connection
