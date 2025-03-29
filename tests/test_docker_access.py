# import httpx
# import pytest
#
#
# @pytest.mark.asyncio
# async def test_service_availability():
#     async with httpx.AsyncClient() as client:
#         response = await client.get("http://localhost:8000")
#     assert response.status_code == 307
