import uuid
from typing import cast, Literal

from databases import Database
from sqlalchemy import select, insert, delete, desc, asc
from db.models import Lamp, Manufacturer
from core.exceptions import BadRequestError, NotFoundError
from schemas.lamp import LampDtlInfo, LampIN, LampOUT


class LampController:

    def __init__(self, db: Database):
        self.db = db

    async def add_lamp(self, lamp: LampIN) -> LampDtlInfo:
        lamp_id = uuid.uuid4()
        manufacturer_query = select(Manufacturer.id).where(Manufacturer.manufacturer == lamp.manufacturer)
        manufacturer_id = await self.db.fetch_one(manufacturer_query)
        if not manufacturer_id:
            raise NotFoundError("No such manufacturer found.")

        article_query = select(Lamp.article).where(Lamp.article == lamp.article)
        article_lamp = await self.db.fetch_one(article_query)
        if article_lamp:
            raise NotFoundError("An object with this article already exists.")

        await self.db.execute(insert(Lamp).values(id=lamp_id, article=lamp.article, price=lamp.price, shape=lamp.shape,
                                                  base=lamp.base, temperature=lamp.temperature,
                                                  manufacturer_id=manufacturer_id[0]))
        finish_query = (select(Lamp.create_at, Manufacturer.country)
                        .join(Manufacturer, cast("ColumnElement[bool]", Lamp.manufacturer_id == Manufacturer.id)))
        finish = await self.db.fetch_one(finish_query)
        return LampDtlInfo(id=str(lamp_id), article=lamp.article, manufacturer=lamp.manufacturer, price=lamp.price,
                           shape=lamp.shape, base=lamp.base, temperature=lamp.temperature,
                           create_at=str(finish["create_at"]),
                           manufacturer_id=str(manufacturer_id[0]),
                           country=finish["country"])

    async def get_all(self, sort: Literal['asc', 'desc'] = "desc") -> list[LampOUT]:
        query = (
            select(
                Lamp.id,
                Lamp.article,
                Lamp.price,
                Manufacturer.manufacturer,
                Manufacturer.country
            )
            .join(Manufacturer, cast("ColumnElement[bool]", Lamp.manufacturer_id == Manufacturer.id))
            .order_by(desc(Lamp.price) if sort == "desc" else asc(Lamp.price))
        )
        rows = await self.db.fetch_all(query)
        result = [dict(row) for row in rows]
        return [
            LampOUT(id=str(row.get("id")), article=row.get("article"),
                    manufacturer=row.get("manufacturer"), price=row.get("price"),
                    country=row.get("country"))
            for row in result
        ]

    async def get_by_article(self, lamp_article: int) -> LampDtlInfo:
        article_query = select(Lamp.article).where(Lamp.article == lamp_article)
        article_lamp = await self.db.fetch_one(article_query)
        if not article_lamp:
            raise NotFoundError("An object with such an ID will not be found.")

        query = (select(Lamp, Manufacturer.manufacturer, Manufacturer.country)
                 .join(Manufacturer, cast("ColumnElement[bool]", Lamp.manufacturer_id == Manufacturer.id))
                 .where(Lamp.article == lamp_article))
        row = await self.db.fetch_one(query)
        return LampDtlInfo(id=str(row["id"]),
                           article=row["article"],
                           manufacturer=row["manufacturer"],
                           price=row["price"],
                           shape=row["shape"],
                           base=row["base"],
                           temperature=row["temperature"],
                           create_at=str(row["create_at"]),
                           country=row["country"])

    async def del_by_article(self, lamp_article: int) -> None:
        article_query = select(Lamp.article).where(Lamp.article == lamp_article)
        article_lamp = await self.db.fetch_one(article_query)
        if not article_lamp:
            raise NotFoundError("An object with such an ID will not be found.")

        query = delete(Lamp).where(Lamp.article == lamp_article)
        await self.db.execute(query)


lamp_controller: LampController = None


def get_controller():
    if lamp_controller is None:
        raise BadRequestError('Controller is none.')
    return lamp_controller
