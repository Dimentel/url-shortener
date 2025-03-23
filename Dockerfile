FROM python:3.12

# Установка системных зависимостей под root
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Создание не-root пользователя
RUN useradd -m appuser
WORKDIR /home/appuser/app
RUN chown appuser:appuser /home/appuser/app

# Копирование зависимостей и установка под appuser
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Копирование остальных файлов
COPY --chown=appuser:appuser . .

USER appuser

# Остальные команды
RUN chmod +x docker/*.sh

CMD ["./docker/app.sh"]