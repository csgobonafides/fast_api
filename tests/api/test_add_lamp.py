import pytest
from httpx import AsyncClient
from storages.jsonfilestorage import JsonFileStorage


@pytest.mark.asyncio
async def test_add_lamp_200(xclient: AsyncClient, lamp_db: JsonFileStorage):
    payload = {"name": "PRO", "price": 203.42, "shape": "R50", "base": "E14", "temperature": "ww"}
    response = await xclient.post('/lamps/', json=payload)
    assert response.status_code == 201
    assert response.json() == {
        "name": "PRO",
        "price": 203.42,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww"
    }
    assert await lamp_db.get('4') == {"id": "4", "name": "PRO", "price": 203.42, "shape": "R50", "base": "E14", "temperature": "ww"}

@pytest.mark.asyncio
async def test_add_lamp_dubl_403(xclient: AsyncClient):
    payload = {"name": "gauss", "price": 134.2, "shape": "R50", "base": "E14", "temperature": "cw"}
    response = await xclient.post('/lamps/', json=payload)
    assert response.status_code == 403, response.text


@pytest.mark.asyncio
async def test_add_lamp_non_type_422_price(xclient: AsyncClient):
    payload = {"name": "gausss", "price": "qwe", "shape": "R50", "base": "E14", "temperature": "cw"}
    response = await xclient.post('/lamps/', json=payload)
    assert response.status_code == 422, response.text

@pytest.mark.asyncio
async def test_add_lamp_non_type_422_name(xclient: AsyncClient):
    payload = {"name": 123, "price": 134.2, "shape": "R50", "base": "E14", "temperature": "cw"}
    response = await xclient.post('/lamps/', json=payload)
    assert response.status_code == 422, response.text