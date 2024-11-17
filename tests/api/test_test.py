import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_xclient_debug_exceptions(xclient_debug: AsyncClient):
    with pytest.raises(ZeroDivisionError):
        response = await xclient_debug.get('/items/exceptions')


@pytest.mark.asyncio
async def test_xclient_exceptions(xclient: AsyncClient):
    response = await xclient.get('/items/exceptions')
    assert response.status_code == 500