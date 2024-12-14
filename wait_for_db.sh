#!/bin/sh

# Ждем готовности базы данных
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL is up and running!"
exec "$@"
