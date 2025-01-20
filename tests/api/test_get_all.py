import pytest
from httpx import AsyncClient
from unittest.mock import ANY

from db.models import Lamp, Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_lamp")
async def test_get_all(xclient: AsyncClient, lamp: Lamp, manufacturer: Manufacturer):
    response = await xclient.get('/lamp/')
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": str(lamp.id),
            "article": lamp.article,
            "price": lamp.price,
            "shape": lamp.shape,
            "base": lamp.base,
            "temperature": lamp.temperature,
            "create_at": ANY,
            "manufacturer": {
                "id": str(manufacturer.id),
                "name": manufacturer.name,
                "country": manufacturer.country
            }
        }
    ]
