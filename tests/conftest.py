import pytest
import pytest_asyncio
from httpx import AsyncClient
from typing import Generator
from fastapi.testclient import TestClient

from app import app


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def xclient(client) -> AsyncClient:
    async with AsyncClient(app=app, base_url=client.base_url) as cli:
        yield cli