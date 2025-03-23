#!/bin/bash

# Ждём доступности PostgreSQL (теперь pg_isready доступен)
until pg_isready -h db -U user -d dbname; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done

# Ждём готовности Redis
until redis-cli -h redis ping; do
  echo "Waiting for Redis..."
  sleep 2
done

# Применяем миграции
alembic upgrade head

# Запускаем приложение
cd src || { echo "Failure to change directory to src"; exit 1; }

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000