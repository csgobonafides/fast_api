import uuid

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.orm import declarative_base
from pathlib import Path
from alembic import command
from alembic.config import Config
from databases import Database
from db.models import Lamp, Manufacturer
import controllers.lamp as lamp_module
import controllers.manufacturer as manufacter_module

from app import app

Base = declarative_base()


@pytest_asyncio.fixture(scope='module')
async def test_db():
    db = Database('postgresql://mamba:mamba@localhost:7432/test_db')
    await db.connect()

    dir = Path(__file__).parent.parent
    alembic_cfg = Config(dir / 'alembic.ini')
    command.upgrade(alembic_cfg, "head")

    one_id = uuid.uuid4()
    await db.execute(insert(Manufacturer).values(id=one_id, manufacturer='gauss', country='usa'))
    two_id = uuid.uuid4()
    await db.execute(insert(Manufacturer).values(id=two_id, manufacturer='iek', country='russia'))
    three_id = uuid.uuid4()
    await db.execute(insert(Manufacturer).values(id=three_id, manufacturer='saffit', country='china'))

    id_one = uuid.uuid4()
    manuf_one = await db.execute(select(Manufacturer.id).where(Manufacturer.manufacturer == 'gauss'))
    await db.execute(insert(Lamp).values(id=id_one, article=111111, price=23.6,  shape='R39', base='E14',
                                         temperature='cw', manufacturer_id=manuf_one, ))
    id_two = uuid.uuid4()
    manuf_two = await db.execute(select(Manufacturer.id).where(Manufacturer.manufacturer == 'iek'))
    await db.execute(insert(Lamp).values(id=id_two, article=222222, price=150.2, shape='R63', base='E27',
                                         temperature='ww', manufacturer_id=manuf_two, ))

    id_three = uuid.uuid4()
    manuf_three = await db.execute(select(Manufacturer.id).where(Manufacturer.manufacturer == 'gauss'))
    await db.execute(insert(Lamp).values(id=id_three, article=333333, price=54, shape='C37', base='E14',
                                         temperature='cw', manufacturer_id=manuf_three, ))

    id_four = uuid.uuid4()
    manuf_four = await db.execute(select(Manufacturer.id).where(Manufacturer.manufacturer == 'saffit'))
    await db.execute(insert(Lamp).values(id=id_four, article=444444, price=250.3, shape='G45', base='E27',
                                         temperature='nw', manufacturer_id=manuf_four, ))

    yield db

    await db.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
    await db.disconnect()


@pytest_asyncio.fixture(autouse=True)
async def lamp_controller(test_db) -> lamp_module.LampController:
    lamp_module.lamp_controller = lamp_module.LampController(test_db)
    yield lamp_module.lamp_controller


@pytest_asyncio.fixture(autouse=True)
async def manufacter_controller(test_db) -> manufacter_module.ManufacturerController:
    manufacter_module.manufacturer_controller = manufacter_module.ManufacturerController(test_db)
    yield manufacter_module.manufacturer_controller


@pytest_asyncio.fixture
async def xclient() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8010") as cli:
        yield cli
