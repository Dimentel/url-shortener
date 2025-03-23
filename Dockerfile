FROM python:3.12-slim

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    netcat && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копирование требований первым для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов
COPY . .

# Права на скрипты
RUN chmod +x docker/*.sh

CMD ["./docker/app.sh"]