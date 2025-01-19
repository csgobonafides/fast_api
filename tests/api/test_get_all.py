import pytest
from httpx import AsyncClient

from db.models import Lamp, Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_lamp")
async def test_get_all(xclient: AsyncClient, lamp: Lamp, manufacturer: Manufacturer):
    response = await xclient.get('/lamps/')
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id":str(lamp.id),
            "article":lamp.article,
            "price":lamp.price,
            "shape":lamp.shape,
            "base":lamp.base,
            "temperature":lamp.temperature,
            "manufacturer": {
                "id": str(manufacturer.id),
                "name": manufacturer.name,
                "country": manufacturer.country
            }
        }
    ]


@pytest.mark.asyncio
async def test_get_all_two(xclient: AsyncClient):
    response = await xclient.get('/lamps/')
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3, response.text
    assert response.json() == [
                {
                    'article': 112233,
                    'id': '1',
                    'name': 'gauss',
                    'price': 134.2,
                },
                {
                    'article': 441122,
                    'id': '2',
                    'name': 'sweko',
                    'price': 89.0,
                },
                {
                    'article': 379283,
                    'id': '3',
                    'name': 'uniel',
                    'price': 13.2,
                },
           ]
