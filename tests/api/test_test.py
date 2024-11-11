import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_xclient_debug_exceptions(xclient_debug: AsyncClient):
    response = await xclient_debug.get('/items/exceptions/')
    assert response.status_code == 200