# import pytest
# from unittest.mock import patch
# from src.tasks.tasks import send_email
#
#
# @pytest.mark.anyio
# @patch("smtplib.SMTP_SSL")
# async def test_email_task(mock_smtp):
#     # Тестируем успешную отправку
#     test_email = "user@example.com"
#     send_email(test_email)
#
#     # Проверяем вызовы SMTP
#     mock_smtp.return_value.login.assert_called_once()
#     mock_smtp.return_value.send_message.assert_called_once()
#
#
# @pytest.mark.anyio
# @patch("smtplib.SMTP_SSL", side_effect=Exception("Connection failed"))
# async def test_email_retry(mock_smtp):
#     # Тестируем ретрай при ошибке
#     with pytest.raises(Exception):
#         send_email("user@example.com")
#     assert mock_smtp.call_count == 3  # 3 попытки согласно настройкам
