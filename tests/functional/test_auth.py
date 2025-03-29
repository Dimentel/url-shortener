import pytest
from fastapi import status

from logger import logger


@pytest.mark.anyio
async def test_protected_route_access(client, auth_client):

    # Неаутентифицированный доступ
    non_auth_response = await client.get("/protected-route")
    assert non_auth_response.status_code == status.HTTP_401_UNAUTHORIZED

    # Аутентифицированный доступ
    auth_response = await auth_client.get("/protected-route")
    logger.info(auth_response)
    assert auth_response.status_code == status.HTTP_200_OK
    assert "Hello" in auth_response.text

@pytest.mark.anyio
async def test_unprotected_route_access(client, auth_client):

    # Неаутентифицированный доступ
    non_auth_response = await client.get("/unprotected-route")
    assert non_auth_response.status_code == status.HTTP_200_OK
    assert "Hello, anonym" in non_auth_response.text

    # Аутентифицированный доступ
    auth_response = await auth_client.get("/unprotected-route")
    logger.info(auth_response)
    assert auth_response.status_code == status.HTTP_200_OK
    assert "Hello, anonym" in auth_response.text
