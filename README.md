# Aiven Test
`Clicker` is a boilerplate for [Click](https://palletsprojects.com/p/click/) based command line tool.

Create commands in `commands` folder.

# Setup
Rename `docker-compose.example.yml` to `docker-compose.yml`. Set the following environment variables.

```yml
environment:
  KAFKA_HOST: "<kafka host>"
  KAFKA_CA_FILE: "<path to ca certificate file>"
  KAFKA_CERT_FILE: "<path to access certificate file>"
  KAFKA_KEY_FILE: "<path to access key file>"
  KAFKA_TOPIC: "<kafka topic>"
  KAFKA_CLIENT_ID: "<kafka client id>"
  KAFKA_GROUP_ID: "<kafka group id>"
  DATABASE_URL: "<postgres database url>"
```

To create database tables and kafka topic run the following command.
```bash
docker-compose run aiven ./manage.py setup
```

# Producer

To run the producer

```bash
docker-compose run aiven ./manage.py producer --url="https://google.com"
```

Here are the available options you can pass to producer

```
  -u, --url TEXT          [required]    The URL you want to monitor
  -i, --interval INTEGER  [default: 30] How frequently you want to monitor. Interval in seconds.
  -t, --timeout INTEGER   [default: 3]  Request timeout time in seconds
  -r, --regex TEXT        [optional]    The regular expression you want to test the page with
  --help                  Show help
```

# Consumer

To run the consumer

```bash
docker-compose run aiven ./manage.py consumer
```

Here are the available options you can pass to the consumer

```
  -f, --frequency INTEGER  [default: 5] How frequently you want to store the consumed data to DB (In seconds).
  --help                   Show help
```
