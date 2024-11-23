import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_lamp(xclient: AsyncClient):
    payload = {"name": "sweko", "price": 89, "shape": "A60", "base": "E27", "temperature": "nw"}
    response = await xclient.post('/items/add_lamp', json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "name": "sweko",
        "price": 89,
        "shape": "A60",
        "base": "E27",
        "temperature": "nw"
    }

@pytest.mark.asyncio
async def test_add_lamp_dubl(xclient: AsyncClient):
    payload = {"name": "gauss", "price": 134.2, "shape": "R50", "base": "E14", "temperature": "cw"}
    response = await xclient.post('/items/add_lamp', json=payload)
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_add_lamp_non_type(xclient: AsyncClient):
    payload = {"name": "gausss", "price": "qwe", "shape": "R50", "base": "E14", "temperature": "cw"}
    response = await xclient.post('/items/add_lamp', json=payload)
    assert response.status_code == 422, response.text