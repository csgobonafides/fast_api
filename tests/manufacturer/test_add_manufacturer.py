import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_manufacturer_200(xclient: AsyncClient, test_db):
    payload = {"manufacturer": "gauss", "country": "string"}
    response = await xclient.post('/manufacturer/', json=payload)
    assert response.status_code == 200
