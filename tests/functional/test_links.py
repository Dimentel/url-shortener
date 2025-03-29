import pytest
from fastapi import status

from logger import logger
from schemas import LinkCreate
from src.models import Link
from datetime import datetime, timedelta


@pytest.mark.anyio
async def test_create_anonymous_link(client, auth_client, session):
    test_link_1 = {
        "original_url": "https://google.com",
        "custom_alias": None,
        "expires_at": None,
    }

    test_link_2 = {
        "original_url": "https://nlmk.com",
        "custom_alias": None,
        "expires_at": None,
    }

    non_auth_response = await client.post("/links/shorten/anonymous", json=test_link_1)

    assert non_auth_response.status_code == status.HTTP_200_OK
    non_auth_data = non_auth_response.json()
    assert len(non_auth_data["short_code"]) == 6
    assert "id" in non_auth_data
    assert "original_url" in non_auth_data
    assert "created_at" in non_auth_data
    assert "expires_at" in non_auth_data

    auth_response = await auth_client.post("/links/shorten/anonymous", json=test_link_2)
    assert auth_response.status_code == status.HTTP_200_OK
    auth_data = auth_response.json()
    assert len(auth_data["short_code"]) == 6
    assert "id" in auth_data
    assert "original_url" in auth_data
    assert "created_at" in auth_data
    assert "expires_at" in auth_data


@pytest.mark.anyio
async def test_create_link(client, auth_client, session):
    test_link_1 = {
        "original_url": "https://ya.ru",
        "custom_alias": None,
        "expires_at": None
    }

    test_link_2 = {
        "original_url": "https://mail.ru/",
        "custom_alias": None,
        "expires_at": None
    }

    non_auth_response = await client.post("/links/shorten", json=test_link_1)
    assert non_auth_response.status_code == status.HTTP_401_UNAUTHORIZED

    auth_response = await auth_client.post("/links/shorten", json=test_link_2)
    logger.info(auth_response.json())
    assert auth_response.status_code == status.HTTP_200_OK
    auth_data = auth_response.json()
    assert "short_code" in auth_data
    assert "id" in auth_data
    assert "original_url" in auth_data
    assert "created_at" in auth_data
    assert "expires_at" in auth_data


@pytest.mark.anyio
async def test_search_link(auth_client, session):
    search_url_substr = {"original_url": "mail"}
    auth_response = await auth_client.get("/links/search", params=search_url_substr)
    assert auth_response.status_code == status.HTTP_200_OK
    url_list = auth_response.json()
    assert len(url_list) > 0
    assert url_list[0]["original_url"] == "https://mail.ru/"

    search_url_substr = {"original_url": "mail1"}
    auth_response = await auth_client.get("/links/search", params=search_url_substr)
    assert auth_response.status_code == status.HTTP_200_OK
    url_list = auth_response.json()
    assert len(url_list) == 0


# @pytest.mark.anyio
# async def test_link_redirect(client, session):
#     # Создаем тестовую ссылку
#     link = Link(
#         original_url="https://python.org",
#         short_code="py1234",
#         expires_at=datetime.now() + timedelta(days=1)
#         )
#     session.add(link)
#     await session.commit()
#
#     # Проверяем редирект
#     response = await client.get("/links/py1234", follow_redirects=False)
#     assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
#     assert response.headers["location"] == "https://python.org"
#
#
# @pytest.mark.anyio
# async def test_expired_link_redirect(client, session):
#     # Создаем просроченную ссылку
#     link = Link(
#         original_url="https://expired.com",
#         short_code="exp123",
#         expires_at=datetime.now() - timedelta(days=1))
#     session.add(link)
#     await session.commit()
#
#     response = await client.get("/links/exp123")
#     assert response.status_code == status.HTTP_410_GONE
#
