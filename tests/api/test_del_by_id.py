import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_del_by_id(xclient: AsyncClient):
    payload = {'id': '1'}
    response = await xclient.delete("/items/del_by_id", params=payload)
    assert response.status_code == 200