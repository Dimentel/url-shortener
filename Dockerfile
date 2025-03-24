FROM python:3.10

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y \
    postgresql-client-15 \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /url-shortener

# Кэширование зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Права на скрипты
RUN chmod +x docker/*.sh

CMD ["./docker/app.sh"]