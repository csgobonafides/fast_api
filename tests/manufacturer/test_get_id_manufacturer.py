from uuid import uuid4

import pytest
from httpx import AsyncClient

from db.models import Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_get_id_manufacturer_200(xclient: AsyncClient, manufacturer: Manufacturer):
    response = await xclient.get(f"/manufacturer/{manufacturer.id}")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": str(manufacturer.id),
        "name": manufacturer.name,
        "country": manufacturer.country
    }


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_get_id_manufacturer_404(xclient: AsyncClient, manufacturer: Manufacturer):
    response = await xclient.get(f"/manufacturer/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Manufacturer not found."}
