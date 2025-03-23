from redis import asyncio as aioredis

# Глобальная переменная для Redis-клиента
redis_client: aioredis.Redis | None = None


async def init_redis():
    """Инициализация Redis."""
    global redis_client
    redis_client = aioredis.from_url("redis://localhost:6379")


async def get_redis_client() -> aioredis.Redis:
    """Возвращает Redis-клиент."""
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized.")
    return redis_client
