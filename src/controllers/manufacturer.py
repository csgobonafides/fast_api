import uuid
from databases import Database
from sqlalchemy import select, insert, delete
from db.models import Manufacturer
from core.exceptions import BadRequestError, NotFoundError
from schemas.manufacturer import ManufacturerRequest, ManufacturerResponse


class ManufacturerController:

    def __init__(self, db: Database):
        self.db = db

    async def add_manufacturer(self, manufacturer: ManufacturerRequest) -> ManufacturerResponse:
        list_id = uuid.uuid4()
        await self.db.execute(insert(Manufacturer).values(id=list_id, manufacturer=manufacturer.manufacturer,
                                                          country=manufacturer.country))
        return ManufacturerResponse(id=str(list_id), manufacturer=manufacturer.manufacturer,
                                    country=manufacturer.country)

    async def get_all_manufacturer(self) -> list[ManufacturerResponse]:
        rows = await self.db.fetch_all(select(Manufacturer))
        result = [dict(row) for row in rows]
        return [
            ManufacturerResponse(id=str(row.get("id")), manufacturer=row.get("manufacturer"),
                                 country=row.get("country"))
            for row in result
        ]

    async def get_by_id(self, manufacturer_id: uuid.UUID) -> ManufacturerResponse:
        query = select(Manufacturer).where(Manufacturer.id == manufacturer_id)
        row = await self.db.fetch_one(query)
        if not row:
            raise NotFoundError('An object with such an ID will not be found.')
        return ManufacturerResponse(id=str(row["id"]), manufacturer=row["manufacturer"],
                                    country=row["country"])

    async def del_by_id(self, manufacturer_id: uuid.UUID) -> None:
        query = delete(Manufacturer).where(Manufacturer.id == manufacturer_id)
        existing_manufacturer = select(Manufacturer).where(Manufacturer.id == manufacturer_id)
        row = await self.db.fetch_one(existing_manufacturer)
        if not row:
            raise NotFoundError("An object with such an ID will not be found.")
        await self.db.execute(query)


manufacturer_controller: ManufacturerController = None


def get_controller():
    if manufacturer_controller is None:
        raise BadRequestError("Controller is none.")
    return manufacturer_controller
