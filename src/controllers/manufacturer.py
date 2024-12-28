import logging
import uuid
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.connector import DatabaseConnector
from db.models import Manufacturer
from core.exceptions import BadRequestError, NotFoundError
from schemas.manufacturer import ManufacturerRequest, ManufacturerResponse

logger = logging.getLogger("manufacturer_router")


class ManufacturerController:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    async def add_manufacturer(self, manufacturer: ManufacturerRequest) -> ManufacturerResponse:
        logger.info(f"Requested to create a manufacturer {manufacturer.name}.")

        manufact_id = uuid.uuid4()
        async with self.db.session_maker() as session:
            try:
                manufact = Manufacturer(
                    id=manufact_id,
                    name=manufacturer.name,
                    country=manufacturer.country
                )
                session.add(manufact)
                await session.commit()
            except IntegrityError:
                logger.error(f"Attempting to add an existing manufacturer {manufacturer.name}.")
                raise NotFoundError("An object with this name already exists.")
        return ManufacturerResponse(id=manufact_id, name=manufacturer.name,
                                    country=manufacturer.country)

    async def get_all_manufacturer(self) -> list[ManufacturerResponse]:
        logger.info("A list of all manufacturers was requested.")

        async with self.db.session_maker() as session:
            cursor = await session.execute(select(Manufacturer))
            manufacts = cursor.scalars().all()
        return [
            ManufacturerResponse(id=man.id, name=man.name,
                                 country=man.country)
            for man in manufacts
        ]

    async def get_by_id(self, name_id: uuid.UUID) -> ManufacturerResponse:
        logger.info(f"Manufacturer with ID requested {name_id}.")

        async with self.db.session_maker() as session:
            manufact = await session.get(Manufacturer, name_id)
        if not manufact:
            raise NotFoundError("Manufacturer not found.")
        return ManufacturerResponse(id=manufact.id, name=manufact.name,
                                    country=manufact.country)

    async def del_by_id(self, name_id: uuid.UUID) -> None:
        async with self.db.session_maker() as session:
            manufact = await session.get(Manufacturer, name_id)
            if not manufact:
                raise NotFoundError("Manufacturer not found.")
            await session.delete(manufact)
            await session.commit()

        logger.info(f"The manufacturer with ID {name_id} was removed.")


manufacturer_controller: ManufacturerController = None


def get_controller():
    if manufacturer_controller is None:
        raise BadRequestError("Controller is none.")
    return manufacturer_controller
