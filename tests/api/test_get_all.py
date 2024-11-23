import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all(xclient: AsyncClient):
    response = await xclient.get('/items/get_all')
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": "1",
            "name": "sweko",
            "price": 89.0,
        },
        {
            "id": "2",
            "name": "gauss",
            "price": 134.2,
        }
    ]