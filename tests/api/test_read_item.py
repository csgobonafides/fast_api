import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_item(xclient: AsyncClient, null=None):
    response = await xclient.get('/items/')
    assert response.status_code == 200
    assert response.json() == [
  {
    "name": "Portal Gun",
    "description": null,
    "price": 42,
    "tax": null,
    "tags": []
  },
  {
    "name": "Plumbus",
    "description": null,
    "price": 32,
    "tax": null,
    "tags": []
  }
]