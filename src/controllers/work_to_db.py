from _exceptions.to_exception import ForbiddenError, NotFoundError
from storages.jsonfilestorage import JsonFileStorage
from schemas.lamps import LampIN, LampDtlInfo, LampOUT

class Controller:

    def __init__(self, product_db):
        self.product_db: JsonFileStorage = product_db

    async def add_lamp(self, lamp: LampIN) -> LampIN:
        if not await self.product_db.check_lamp(lamp):
            raise ForbiddenError('This product already exists in the database.')

        last_id = await self.product_db.check_last_id()
        result = {"id": last_id, "name": lamp.name, "price": lamp.price, "shape": lamp.shape, "base": lamp.base, "temperature": lamp.temperature}
        await self.product_db.add(last_id, result)
        return result


    async def get_all(self) -> list[LampOUT]:
        lamp = await self.product_db.get_all()
        return lamp


    async def get_by_id(self, lamp_id: str) -> LampDtlInfo:
        return await self.product_db.get(lamp_id)


    async def del_by_id(self, lamp_id: str):
        return await self.product_db.delete(lamp_id)






controller = None

def get_controller():
    if controller is None:
        raise ForbiddenError('Controller is none.')
    return controller


class CarController:
    pass