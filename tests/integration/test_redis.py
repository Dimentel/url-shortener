# import pytest
# from unittest.mock import AsyncMock, patch
# from src.redis_client import get_redis_client
#
#
# @pytest.mark.anyio
# async def test_redis_connection_error():
#     """Тест ошибки при отсутствии инициализации Redis"""
#     with pytest.raises(RuntimeError, match="Redis client is not initialized"):
#         await get_redis_client()
#
#
# @pytest.mark.anyio
# async def test_redis_successful_connection():
#     """Тест успешного подключения к Redis"""
#     mock_redis = AsyncMock()
#
#     # Патчим глобальную переменную redis_client
#     with patch("src.redis_client.redis_client", new=mock_redis):
#         result = await get_redis_client()
#         assert result == mock_redis
#
#
# @pytest.mark.anyio
# async def test_redis_cache_operations():
#     """Тест операций кэширования"""
#     test_data = {"key": "test_value"}
#
#     mock_redis = AsyncMock()
#     mock_redis.get.return_value = None
#     mock_redis.set.return_value = True
#
#     with patch("src.redis_client.redis_client", new=mock_redis):
#         # Проверяем установку значения
#         client = await get_redis_client()
#         await client.set("test_key", test_data)
#
#         # Проверяем получение значения
#         await client.get("test_key")
#         mock_redis.set.assert_awaited_once()
#         mock_redis.get.assert_awaited_once()
#
#
# @pytest.mark.anyio
# async def test_redis_cache_expiration(mock_redis):
#     """Тест expiration времени кэша"""
#     mock_client = AsyncMock()
#     mock_redis.return_value = mock_client
#
#     client = await get_redis_client()
#     await client.set("key", "value", expire=60)
#
#     mock_client.set.assert_awaited_once_with("key", "value", ex=60)
