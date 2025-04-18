from celery import Celery
from src.config import (
    SMTP_USER,
    SMTP_PASSWORD,
    SMTP_HOST,
    SMTP_PORT,
    REDIS_HOST,
    REDIS_PORT,
)
import smtplib
from email.message import EmailMessage

from src.logger import logger

celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")


def get_template_email(username: str):
    """Создание HTML-шаблона для email."""
    msg = EmailMessage()
    msg["Subject"] = "Уведомление от URL Shortener"
    msg["From"] = SMTP_USER
    msg["To"] = username  # Используем email пользователя
    msg.set_content(
        "<div>"
        f'<h1 style="color: red;">Здравствуйте, {username}. Ваша ссылка была успешно создана или изменена.</h1>'
        "</div>",
        subtype="html",
    )
    return msg


@celery.task(default_retry_delay=5, max_retries=3)
def send_email(email: str):
    """Отправка email."""
    msg = get_template_email(email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        try:
            server.send_message(msg)
        except Exception as e:
            logger.warning("Failed to send email: %s", e)
            send_email.retry()
