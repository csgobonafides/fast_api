import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all(xclient: AsyncClient):
    response = await xclient.get('/items/get_all')
    assert response.status_code == 200