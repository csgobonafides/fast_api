import pytest
from unittest.mock import ANY
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_manufacturer_201(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": "gauss", "country": "china"}
    response = await xclient.post('/manufacturer/', json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data == {
        "id": ANY,
        "name": "gauss",
        "country": "china"
    }
    async with test_db.session_maker() as session:
        manufact_db = await session.get(Manufacturer, data["id"])
        assert manufact_db.name == data["name"]
        assert manufact_db.country == data["country"]


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_manufacturer_404(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": "Uniel", "country": "USA"}
    response = await xclient.post('/manufacturer/', json=payload)
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "An object with this name already exists."}


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_manufacturer_422(xclient: AsyncClient, test_db: DatabaseConnector):
    payload = {"name": 123, "country": "china"}
    response = await xclient.post('/manufacturer/', json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "string_type",
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "Input should be a valid string",
                "input": 123
            }
        ]
    }
