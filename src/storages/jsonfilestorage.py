import json
from storages.base import CacheStorage
from _exceptions.to_exception import ForbiddenError, NotFoundError
from schemas.lamps import LampIN, LampDtlInfo


class JsonFileStorage(CacheStorage):
    def __init__(self, file_path = None):
        self.file_path = file_path
        self.data = {}

    async def connect(self):
        if self.file_path is None:
            return

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    async def disconnect(self):
        if self.file_path is None:
            return
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)


    async def check_lamp(self, lamp: LampIN) -> bool:
        val = {"name": lamp.name, "price": lamp.price, "shape": lamp.shape, "base": lamp.base, "temperature": lamp.temperature}
        for lamp_data in self.data.values():
            comparison_data = {k: lamp_data[k] for k in lamp_data if k != 'id'}
            if comparison_data == val:
                return False
            else:
                return True

    async def check_last_id(self):
        if list(self.data.keys()) == []:
            return "1"
        else:
            next_id = str(int(list(self.data.keys())[-1]) + 1)
            return next_id

    async def add(self, key: str, value: dict) -> None:
        if key in self.data:
            raise ForbiddenError('Ключ уже существует.')
        self.data[key] = value

    async def get_all(self):
        return list(self.data.values())

    async def get(self, key: str) -> LampDtlInfo:
        if key not in self.data:
            raise NotFoundError("Такого ключа не найдено.")
        return self.data.get(key)

    async def delete(self, key: str):
        if key not in self.data:
            raise NotFoundError('Такого ключа не найдено.')
        self.data.pop(key)
        if key not in self.data:
            return {"status": 200}