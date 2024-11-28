import pytest
from httpx import AsyncClient
from storages.jsonfilestorage import JsonFileStorage


@pytest.mark.asyncio
async def test_del_by_id_204(xclient: AsyncClient, lamp_db: JsonFileStorage):
    response = await xclient.delete(f"/lamps/3")
    assert response.status_code == 204, response.text
    assert len(lamp_db.data) == 2


@pytest.mark.asyncio
async def test_del_by_id_404(xclient: AsyncClient):
    response = await xclient.delete(f"/lamps/999")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Такого ключа не найдено."}