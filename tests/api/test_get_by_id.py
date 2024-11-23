import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_by_id(xclient: AsyncClient):
    payload = {'id': '2'}
    response = await xclient.post("/items/get_by_id", params=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": "2",
        "name": "gauss",
        "price": 134.2,
        "shape": "R50",
        "base": "E14",
        "temperature": "cw"
    }