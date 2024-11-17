import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(xclient: AsyncClient):
    payload = {'name': 'Bona', 'price': 100}
    response = await xclient.post('/items/', json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "name": "Bona",
        "description": None,
        "price": 100,
        "tax": None,
        "tags": []
    }