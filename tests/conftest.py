import pytest
import pytest_asyncio
from httpx import AsyncClient
import json
import controllers.lamps_controller as lamp_module

from app import app
from storages.jsonfilestorage import JsonFileStorage


@pytest_asyncio.fixture(autouse=True)
async def lamp_controller(tmp_path) -> lamp_module.Controller:
    data = {
        "1": {"id": "1", "name": "gauss", "price": 134.2, "article": 112233, "shape": "R50", "base": "E14", "temperature": "cw"},
        "2": {"id": "2", "name": "sweko", "price": 89.0, "article": 441122, "shape": "A60", "base": "E27", "temperature": "nw"},
        "3": {"id": "3", "name": "uniel", "price": 13.2, "article": 379283, "shape": "A60", "base": "E27", "temperature": "nw"}
    }
    json_file = tmp_path / 'db.json'
    with open(json_file, 'w') as file:
        json.dump(data, file)
    lamp_db = JsonFileStorage(json_file)
    await lamp_db.connect()
    lamp_module.controller = lamp_module.Controller(lamp_db)
    yield lamp_module.controller


@pytest.fixture
def lamp_db(lamp_controller: lamp_module.Controller) -> JsonFileStorage:
    return lamp_controller.product_db


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
