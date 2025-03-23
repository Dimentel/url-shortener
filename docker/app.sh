#!/bin/bash

# Ожидание доступности PostgreSQL
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -U user -d dbname -q; do
  sleep 1
done

# Применение миграций
alembic upgrade head

# Запуск приложения
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120