#!/bin/bash

# Ждём, пока Redis станет доступным
until redis-cli -h redis ping; do
  echo "Waiting for Redis to start..."
  sleep 2
done

cd src || { echo "Failure to change directory to src"; exit 1; }

if [[ "${1}" == "celery" ]]; then
  celery --app=tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=tasks.tasks:celery flower
fi