import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from typing import Generator
from fastapi.testclient import TestClient

from app import app

# @pytest.fixture(scope='session')
# def base_url() -> str:
#     return "http://127.0.0.1:8010"



@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def xclient(client) -> AsyncClient:
    async with AsyncClient(app=app, base_url=client.base_url) as cli:
        yield cli



# @pytest.fixture
# def client() -> Generator:
#     with TestClient(app) as client:
#         yield client
#
#
# @pytest_asyncio.fixture
# async def xclient(client) -> AsyncClient:
#     async with AsyncClient(app=app, base_url=client.base_url) as cli:
#         yield cli


# @pytest_asyncio.fixture
# async def xclient(base_url: str) -> AsyncClient:
#     transport = ASGITransport(app=app, raise_app_exceptions=False)
#     async with AsyncClient(base_url=base_url, transport=transport) as client:
#         yield client
#
# @pytest_asyncio.fixture
# async def xclient_debug(base_url: str) -> AsyncClient:
#     transport = ASGITransport(app=app, raise_app_exceptions=True)
#     async with AsyncClient(base_url=base_url, transport=transport) as client:
#         yield client