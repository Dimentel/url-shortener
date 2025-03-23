from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import secrets
import string
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from src.database import get_async_session
from src.models import Link, User
from src.schemas import LinkCreate, LinkResponse, LinkStatsResponse
from src.tasks.tasks import send_email
from src.auth.users import current_active_user
from src.logger import logger
from src.redis_client import get_redis_client

router = APIRouter(prefix="/links", tags=["links"])


def generate_short_code(length: int = 6) -> str:
    """Генерация случайного короткого кода."""
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


@router.post("/shorten", response_model=LinkResponse)
async def shorten_link_auth(
    link: LinkCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(
        current_active_user
    ),  # Только для авторизованных пользователей
):
    """Создание короткой ссылки (для авторизованных пользователей)."""
    return await _create_link(link, session, user)


@router.post("/shorten/anonymous", response_model=LinkResponse)
async def shorten_link_anon(
    link: LinkCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание короткой ссылки (для неавторизованных пользователей)."""
    return await _create_link(link, session, None)


async def _create_link(
    link: LinkCreate,
    session: AsyncSession,
    user: User | None,
) -> LinkResponse:
    """Общая логика создания ссылки."""
    short_code = link.custom_alias or generate_short_code()
    expires_at = link.expires_at or datetime.now() + timedelta(days=30)

    # Проверка уникальности short_code
    existing_link = await session.execute(
        select(Link).where(Link.short_code == short_code)
    )
    if existing_link.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom alias already exists.",
        )

    # Создаём новую ссылку
    new_link = Link(
        original_url=str(link.original_url),
        short_code=short_code,
        expires_at=expires_at,
        user_id=(
            user.id if user else None
        ),  # Сохраняем user_id, если пользователь авторизован
    )
    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)

    if user:
        logger.info(
            "Пользователь %s создал ссылку: %s -> %s",
            user.email,
            new_link.short_code,
            new_link.original_url,
        )
        # Отправка email пользователю, если он зарегистрирован
        send_email.delay(user.email)
    else:
        logger.info(
            "Незарегистрированный пользователь создал ссылку: %s -> %s",
            new_link.short_code,
            new_link.original_url,
        )
    return LinkResponse.from_orm(new_link)


@router.get("/search", response_model=list[LinkResponse])
async def search_links(
    original_url: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Поиск ссылок по оригинальному URL."""
    result = await session.execute(
        select(Link).where(Link.original_url.contains(original_url))
    )
    links = result.scalars().all()
    return links


@router.get("/{short_code}")
@cache(expire=60)  # Кэшируем на 60 секунд
async def redirect_link(
    short_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Перенаправление по короткой ссылке."""
    result = await session.execute(select(Link).where(Link.short_code == short_code))
    link = result.scalar()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found.",
        )
    if link.expires_at and link.expires_at < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Link has expired.",
        )

    # Увеличиваем счётчик переходов
    link.clicks += 1

    # Обновляем поле last_used_at
    link.last_used_at = datetime.now()

    await session.commit()

    # Перенаправляем на оригинальный URL
    return RedirectResponse(url=link.original_url)


@router.get("/{short_code}/stats", response_model=LinkStatsResponse)
async def get_link_stats(
    short_code: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Получение статистики по короткой ссылке."""
    result = await session.execute(select(Link).where(Link.short_code == short_code))
    link = result.scalar()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found.",
        )

    return LinkStatsResponse(
        original_url=link.original_url,
        created_at=link.created_at,
        clicks=link.clicks,
        last_used_at=link.last_used_at,
    )


@router.put("/{short_code}")
async def update_link(
    short_code: str,
    link: LinkCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    redis_client: aioredis.Redis = Depends(get_redis_client),
):
    """Обновление короткой ссылки."""
    result = await session.execute(select(Link).where(Link.short_code == short_code))
    existing_link = result.scalar()
    if not existing_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found.",
        )

    # Если ссылка создана незарегистрированным пользователем, её может обновить любой зарегистрированный пользователь
    if existing_link.user_id is None or existing_link.user_id == user.id:
        existing_link.original_url = str(link.original_url)
        existing_link.short_code = link.custom_alias
        existing_link.expires_at = link.expires_at or existing_link.expires_at
        await session.commit()

        # Очистка кэша для этой ссылки
        await redis_client.delete(f"links:{short_code}")

        logger.info(
            "Ссылка изменена: %s -> %s стало %s -> %s",
            existing_link.short_code,
            existing_link.original_url,
            link.custom_alias,
            link.original_url,
        )
        # Отправка email пользователю, если он зарегистрирован
        send_email.delay(user.email)

        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this link.",
        )


@router.delete("/{short_code}")
async def delete_link(
    short_code: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    redis_client: aioredis.Redis = Depends(get_redis_client),
):
    """Удаление короткой ссылки."""
    result = await session.execute(select(Link).where(Link.short_code == short_code))
    link = result.scalar()
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found.",
        )

    # Если ссылка создана незарегистрированным пользователем, её может удалить любой зарегистрированный пользователь
    if link.user_id is None or link.user_id == user.id:
        await session.delete(link)
        await session.commit()

        # Очистка кэша для этой ссылки
        await redis_client.delete(f"links:{short_code}")

        # Отправка email пользователю, если он зарегистрирован
        send_email.delay(user.email)

        logger.info(f"Ссылка удалена: %s -> %s", link.short_code, link.original_url)
        return {"status": "success", "message": "Link deleted successfully."}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this link.",
        )
