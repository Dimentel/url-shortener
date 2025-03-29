import asyncio
import uuid
from src.auth.schemas import UserCreate
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from fastapi import status
from unittest.mock import AsyncMock, patch
from asgi_lifespan import LifespanManager

from src.models import Base
from src.database import get_async_session
from src.main import app

# Тестовая БД
TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)

    # Убедимся, что все таблицы удалены перед созданием
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, checkfirst=True)
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    # Очистка после всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all, checkfirst=True)
    await engine.dispose()


@pytest.fixture(scope="session")
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture(scope="session")
async def client(session):
    app.dependency_overrides[get_async_session] = lambda: session

    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as test_client:
            yield test_client


@pytest.fixture(scope="session")
async def client_to_auth(session):
    app.dependency_overrides[get_async_session] = lambda: session

    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as test_client:
            yield test_client


@pytest.fixture(scope="session")
async def registration_data(client_to_auth):

    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_user = UserCreate(
        email=test_email,
        password="strongpassword123",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )

    response = await client_to_auth.post("/auth/register", json=test_user.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

    user_data = response.json()

    assert "id" in user_data
    assert "email" in user_data
    assert "is_active" in user_data
    assert "is_superuser" in user_data
    assert "is_verified" in user_data

    yield user_data


@pytest.fixture(scope="session")
async def auth_client(client_to_auth, registration_data):

    # Логинимся под зарегистрированным пользователем
    login_data = {
        "username": registration_data["email"],
        "password": "strongpassword123",
        "client_id": registration_data["id"],
    }
    response = await client_to_auth.post("/auth/jwt/login", data=login_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()

    access_token = response.json()["access_token"]
    client_to_auth.headers.update({"Authorization": f"Bearer {access_token}"})

    yield client_to_auth


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


# @pytest.fixture(scope="session")
# def mock_redis():
#     with patch("src.redis_client.aioredis.Redis") as mock:
#         mock.return_value = AsyncMock()
#         yield mock
#
#
# @pytest.fixture(scope="session")
# def mock_smtp():
#     with patch("smtplib.SMTP_SSL") as mock:
#         yield mock
#
#
# @pytest.fixture(scope="session")
# def mock_celery():
#     with patch("src.tasks.tasks.celery") as mock:
#         yield mock
