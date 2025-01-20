import pytest
from httpx import AsyncClient

from db.models import Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_list_manufacturer_200(xclient: AsyncClient, manufacturer: Manufacturer):
    response = await xclient.get("/manufacturer/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": str(manufacturer.id),
            "name": manufacturer.name,
            "country": manufacturer.country
        }
    ]
