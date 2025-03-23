from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from typing import AsyncIterator

from src.routers import auth, links, tasks
from src.logger import logger
from src.redis_client import init_redis, get_redis_client


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        # Инициализация Redis для кэширования
        await init_redis()
        redis_client = await get_redis_client()
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        logger.info("Redis initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize Redis: %s", e)
        raise

    yield


app = FastAPI(lifespan=lifespan)


# Подключение роутеров
app.include_router(auth.router)
app.include_router(links.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    """Корневой endpoint, который перенаправляет на документацию Swagger."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app", reload=True, host="0.0.0.0", port=8000, log_level="info"
    )
