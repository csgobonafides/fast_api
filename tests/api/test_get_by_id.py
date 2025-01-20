from uuid import uuid4
from unittest.mock import ANY

import pytest
from httpx import AsyncClient

from db.models import Lamp, Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_lamp")
async def test_get_by_id_200(xclient: AsyncClient, lamp: Lamp, manufacturer: Manufacturer):
    response = await xclient.get(f"/lamp/{lamp.id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
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


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_lamp")
async def test_get_by_id_404(xclient: AsyncClient, lamp: Lamp, manufacturer: Manufacturer):
    response = await xclient.get(f"/lamp/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Lamp not found."}
