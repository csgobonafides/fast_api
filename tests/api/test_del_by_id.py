from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from db.connector import DatabaseConnector
from db.models import Lamp


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_lamp")
async def test_del_by_id_204(xclient: AsyncClient, test_db: DatabaseConnector, lamp_id: UUID):
    response = await xclient.delete(f"/lamp/{lamp_id}")
    assert response.status_code == 204, response.text
    assert response.content == b""
    async with test_db.session_maker() as session:
        deleted_lamp = await session.get(Lamp, lamp_id)
    assert deleted_lamp is None


@pytest.mark.asyncio
async def test_del_by_id_404(xclient: AsyncClient, test_db: DatabaseConnector, lamp_id: UUID):
    response = await xclient.delete(f"/lamp/{uuid4()}")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Lamp not found."}
