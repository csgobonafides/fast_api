from uuid import uuid4
from unittest.mock import ANY

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Lamp, Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_lamp_201(xclient: AsyncClient, test_db: DatabaseConnector, manufacturer: Manufacturer):
    payload = {
        "article": 440101,
        "price": 832.6,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "manufacturer_id": str(manufacturer.id)
    }
    response = await xclient.post('/lamp/', json=payload)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data == {
        "article": 440101,
        "price": 832.6,
        "id": ANY,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "create_at": ANY,
        "manufacturer": {
            "id": str(manufacturer.id),
            "name": manufacturer.name,
            "country": manufacturer.country
        }
    }
    async with test_db.session_maker() as session:
        lmp_db = await session.get(Lamp, data["id"])
    assert lmp_db.article == data["article"]
    assert float(lmp_db.price) == data["price"]
    assert lmp_db.shape == data["shape"]
    assert lmp_db.base == data["base"]
    assert lmp_db.temperature == data["temperature"]
    assert lmp_db.manufacturer_id == manufacturer.id


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
@pytest.mark.usefixtures("prepare_lamp")
async def test_add_lamp_404(xclient: AsyncClient, test_db: DatabaseConnector, lamp:Lamp, manufacturer: Manufacturer):
    payload = {
        "article": lamp.article,
        "price": 832.6,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "manufacturer_id": str(manufacturer.id)
    }
    response = await xclient.post('/lamp/', json=payload)
    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "The lamp with the article already exists."
    }


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
@pytest.mark.usefixtures("prepare_lamp")
async def test_add_lamp_404_1(xclient: AsyncClient, test_db: DatabaseConnector, lamp:Lamp, manufacturer: Manufacturer):
    payload = {
        "article": 440101,
        "price": 832.6,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "manufacturer_id": str(uuid4())
    }
    response = await xclient.post('/lamp/', json=payload)
    assert response.status_code == 404, response.text
    assert response.json() == {
        "detail": "There is no manufacturer with such an ID."
    }


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_lamp_non_type_422_price(xclient: AsyncClient, test_db: DatabaseConnector, manufacturer: Manufacturer):
    payload = {
        "article": 440101,
        "price": "asd",
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "manufacturer_id": str(uuid4())
    }
    response = await xclient.post('/lamp/', json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
                      "detail": [
                          {
                              "type": "float_parsing",
                              "loc": [
                                  "body",
                                  "price"
                              ],
                              "msg": "Input should be a valid number, unable to parse string as a number",
                              "input": "asd"
                          }
                      ]
                  }


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_add_lamp_non_type_422_article(xclient: AsyncClient, test_db: DatabaseConnector, manufacturer: Manufacturer):
    payload = {
        "article": "asd",
        "price": 832.6,
        "shape": "R50",
        "base": "E14",
        "temperature": "ww",
        "manufacturer_id": str(uuid4())
    }
    response = await xclient.post('/lamp/', json=payload)
    assert response.status_code == 422, response.text
    assert response.json() == {
                      "detail": [
                          {
                              "type": "int_parsing",
                              "loc": [
                                  "body",
                                  "article"
                              ],
                              "msg": "Input should be a valid integer, unable to parse string as an integer",
                              "input": "asd"
                          }
                      ]
                  }
