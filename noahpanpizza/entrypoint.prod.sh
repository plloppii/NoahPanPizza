#!/bin/sh

echo "Entering entrypoint.prod.sh"
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres on $DB_HOST:$DB_PORT..."
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

exec "$@"