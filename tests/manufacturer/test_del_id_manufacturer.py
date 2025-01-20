from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Manufacturer


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_del_id_manufacturer_204(xclient: AsyncClient, test_db: DatabaseConnector, manufacturer_id: UUID):
    response = await xclient.delete(f"/manufacturer/{manufacturer_id}")
    assert response.status_code == 204, response.text
    assert response.content == b""
    async with test_db.session_maker() as session:
        deleted_manufact = await session.get(Manufacturer, manufacturer_id)
    assert deleted_manufact is None


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_manufacturer")
async def test_del_id_manufacturer_404(xclient: AsyncClient, test_db: DatabaseConnector, manufacturer_id: UUID):
    response = await xclient.delete(f"/manufacturer/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Manufacturer not found."}
