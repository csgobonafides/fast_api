from core.exceptions import BadRequestError
from storages.jsonfilestorage import JsonFileStorage
from schemas.lamps import LampIN, LampDtlInfo, LampOUT


class Controller:
    def __init__(self, product_db):
        self.product_db: JsonFileStorage = product_db

    async def add_lamp(self, lamp: LampIN) -> LampDtlInfo:
        for lmp in self.product_db.data.values():
            if lmp.get('article') == lamp.article:
                raise BadRequestError('This product already exists in the database.')

        next_id = str(int(max(self.product_db.data.keys())) + 1) if list(self.product_db.data.keys()) != [] else "1"
        result = {
            "id": next_id,
            "name": lamp.name,
            "price": lamp.price,
            "article": lamp.article,
            "shape": lamp.shape,
            "base": lamp.base,
            "temperature": lamp.temperature
        }
        await self.product_db.add(next_id, result)
        return LampDtlInfo(**result)

    async def get_all(self) -> list[LampOUT]:
        raw_lamps = await self.product_db.get_all()
        lamps = [LampOUT(**lamp) for lamp in raw_lamps]
        return lamps

    async def get_by_id(self, lamp_id: str) -> LampDtlInfo:
        lamp = await self.product_db.get(lamp_id)
        return LampDtlInfo(**lamp)

    async def del_by_id(self, lamp_id: str) -> None:
        await self.product_db.delete(lamp_id)


controller = None


def get_controller():
    if controller is None:
        raise BadRequestError('Controller is none.')
    return controller
