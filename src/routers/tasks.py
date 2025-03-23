from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status

from src.database import get_async_session
from src.models import User
from src.tasks.tasks import send_email

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/send-email/{user_id}")
async def trigger_email_task(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Запуск задачи отправки email."""
    # Получаем пользователя из базы данных
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Запуск задачи Celery
    send_email.delay(user.email)
    return {"status": "Email task has been sent."}
