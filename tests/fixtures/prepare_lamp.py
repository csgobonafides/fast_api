from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Lamp


@pytest.fixture
def lamp_id() -> UUID:
    return uuid4()


@pytest.fixture
def lamp(lamp_id: UUID, manufacturer_id: UUID) -> Lamp:
    return Lamp(
        id=lamp_id,
        article=232301,
        price=123.42,
        shape="A60",
        base="E27",
        temperature="nw",
        manufacturer_id=manufacturer_id
    )


@pytest_asyncio.fixture
async def prepare_lamp(test_db: DatabaseConnector, lamp: Lamp, prepare_manufacturer: None) -> None:
    async with test_db.session_maker(expire_on_commit=False) as session:
        session.add(lamp)
        await session.commit()
