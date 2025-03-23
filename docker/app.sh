#!/bin/bash

# Явное ожидание порта PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
until nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL is ready! Applying migrations..."
alembic upgrade head

echo "🚀 Starting application..."
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120