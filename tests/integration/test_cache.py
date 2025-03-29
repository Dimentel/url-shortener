# import pytest
# from src.models import Link
#
#
# @pytest.mark.anyio
# async def test_link_redirect_caching(client, session):
#     # Создаем тестовую ссылку
#     link = Link(original_url="https://example.com", short_code="cache12")
#     session.add(link)
#     await session.commit()
#
#     # Первый запрос - должен кэшироваться
#     response1 = await client.get("/links/cache12")
#     assert "x-cache" not in response1.headers  # Первый запрос не из кэша
#
#     # Второй запрос - должен быть из кэша
#     response2 = await client.get("/links/cache12")
#     assert response2.headers.get("x-cache") == "hit"
