#!/bin/sh

max_attempts=12
attempt=0

while [ $attempt -lt $max_attempts ]; do
  if nc -z mysql 3306; then
    flask db upgrade
    flask run --host=0.0.0.0
    break
  else
    sleep 5
    attempt=$((attempt + 1))
  fi
done

if [ $attempt -eq $max_attempts ]; then
  echo "Connection to mysql:3306 could not established."
fi