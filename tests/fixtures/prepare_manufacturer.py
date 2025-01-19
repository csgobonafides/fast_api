from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Manufacturer


@pytest.fixture
def manufacturer_id() -> UUID:
    return uuid4()


@pytest.fixture
def manufacturer(manufacturer_id: UUID) -> Manufacturer:
    return Manufacturer(
        id=manufacturer_id,
        name="Uniel",
        country="USA"
    )


@pytest_asyncio.fixture
async def prepare_manufacturer(test_db: DatabaseConnector, manufacturer: Manufacturer) -> None:
    async with test_db.session_maker(expire_on_commit=False) as session:
        session.add(manufacturer)
        await session.commit()
