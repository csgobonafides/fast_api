import uuid
import logging
from sqlalchemy.exc import IntegrityError
from schemas.enums import SortOrder, FilterType, DetailType
from sqlalchemy import select, desc, asc
from sqlalchemy.orm import joinedload

from db.connector import DatabaseConnector
from db.models import Lamp, Manufacturer
from core.exceptions import BadRequestError, NotFoundError
from schemas.lamp import LampDtlInfo, LampIN
from schemas.manufacturer import ManufacturerResponse

logger = logging.getLogger("lamp_router")


class LampController:

    def __init__(self, db: DatabaseConnector):
        self.db = db

    async def add_lamp(self, lamp: LampIN) -> LampDtlInfo:
        logger.info(f"Request to create a lamp with article {lamp.article}.")

        lamp_id = uuid.uuid4()
        async with self.db.session_maker() as session:
            try:
                lmp = Lamp(
                    id=lamp_id,
                    article=lamp.article,
                    price=lamp.price,
                    shape=lamp.shape,
                    base=lamp.base,
                    temperature=lamp.temperature,
                    manufacturer_id=lamp.manufacturer_id
                )
                session.add(lmp)
                await session.commit()
            except IntegrityError as IError:
                if 'manufacturer_id' in str(IError.orig):
                    logger.error(f"Attempt to add a manufacturer with a non-existent identifier {lamp.manufacturer_id}.")
                    raise NotFoundError("There is no manufacturer with such an ID.")
                elif 'article' in str(IError.orig):
                    logger.error(f"The lamp with the article {lamp.article} already exists.")
                    raise NotFoundError("The lamp with the article already exists.")
                else:
                    logger.error("An unexpected integrity error occurred.")
                    raise IError.detail
        return await self.get_by_id(lamp_id)

    async def get_all(self, sort: SortOrder = SortOrder.desc,
                      filters: FilterType = None,
                      detail: DetailType = None
                      ) -> list[LampDtlInfo]:
        logger.info("Request a list of light bulbs.")

        async with self.db.session_maker() as session:
            if filters and detail:
                if filters == 'shape' and detail not in ['A60', 'C37', 'G45', 'R39', 'R50', 'R63']:
                    raise BadRequestError
                if filters == 'base' and detail not in ['E40', 'E27', 'E14']:
                    raise BadRequestError
                if filters == 'temperature' and detail not in ['ww', 'nw', 'cw']:
                    raise BadRequestError
                cursor = await session.execute(
                    select(Lamp, Manufacturer).options(joinedload(Lamp.manufacturer))
                    .where(getattr(Lamp, filters) == detail)
                    .order_by(desc(Lamp.price) if sort == "desc" else asc(Lamp.price))
                )
            else:
                cursor = await session.execute(
                    select(Lamp, Manufacturer).options(joinedload(Lamp.manufacturer))
                    .order_by(desc(Lamp.price) if sort == "desc" else asc(Lamp.price)))
            lmps = cursor.scalars().all()
        return [LampDtlInfo(id=lmp.id,
                            article=lmp.article,
                            price=lmp.price,
                            shape=lmp.shape,
                            base=lmp.base,
                            temperature=lmp.temperature,
                            create_at=str(lmp.create_at),
                            manufacturer=ManufacturerResponse(
                                id=lmp.manufacturer.id,
                                name=lmp.manufacturer.name,
                                country=lmp.manufacturer.country),
                            )
                for lmp in lmps
        ]

    async def get_by_id(self, lamp_id: uuid.UUID) -> LampDtlInfo:
        logger.info(f"Request for lamp by ID {lamp_id}.")

        async with self.db.session_maker() as session:
            lmp = await session.get(Lamp, lamp_id, options=[joinedload(Lamp.manufacturer)])
            if not lmp:
                raise NotFoundError("Lamp not found.")
            return LampDtlInfo(id=lamp_id,
                               article=lmp.article,
                               price=lmp.price,
                               shape=lmp.shape,
                               base=lmp.base,
                               temperature=lmp.temperature,
                               create_at=str(lmp.create_at),
                               manufacturer=ManufacturerResponse(
                                   id=lmp.manufacturer.id,
                                   name=lmp.manufacturer.name,
                                   country=lmp.manufacturer.country))

    async def del_by_id(self, lamp_id: uuid.UUID) -> None:
        async with self.db.session_maker() as session:
            lmp = await session.get(Lamp, lamp_id)
            if not lmp:
                raise NotFoundError("Lamp not found.")
            await session.delete(lmp)
            await session.commit()
            logger.info(f"The lamp with the ID {lamp_id} has been removed.")


lamp_controller: LampController = None


def get_controller():
    if lamp_controller is None:
        raise BadRequestError('Controller is none.')
    return lamp_controller
