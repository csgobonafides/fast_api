import pytest
import pytest_asyncio
from httpx import AsyncClient

import controllers.lamp as lamp_module
import controllers.manufacturer as manufacturer_module
from app import app

from core.settings import get_settings, Settings
from db.connector import DatabaseConnector

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_manufacturer",
    "fixtures.prepare_lamp",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest_asyncio.fixture(autouse=True)
async def lamp_controller(test_db: DatabaseConnector) -> lamp_module.LampController:
    lamp_module.lamp_controller = lamp_module.LampController(test_db)
    yield lamp_module.lamp_controller


@pytest_asyncio.fixture(autouse=True)
async def manufacturer_controller(test_db: DatabaseConnector) -> manufacturer_module.ManufacturerController:
    manufacturer_module.manufacturer_controller = manufacturer_module.ManufacturerController(test_db)
    yield manufacturer_module.manufacturer_controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
