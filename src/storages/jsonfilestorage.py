import json
from src.storages.base import CacheStorage
from src._exceptions.to_exception import ForbiddenError, NotFoundError
from src.schemas.lamps import LampIN


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
        for lamp_data in self.data.get('value')[0].values():
            comparison_data = {k: lamp_data[k] for k in lamp_data if k != 'id'}
            if comparison_data == val:
                return False
            else:
                return True

    async def check_last_id(self) -> int:
        id = self.data.get('id')
        next_id = 1 + id
        self.data['id'] = next_id
        return next_id

    async def add(self, key: str, value: dict) -> None:
        if key in self.data:
            raise ForbiddenError('Ключ уже существует.')
        self.data.get("value")[0][key] = value

    async def get_all(self):
        return list(self.data.get("value")[0].values())

    async def get(self, key: int):
        if str(key) not in self.data.get("value")[0].keys():
            raise NotFoundError("Такого ключа не найдено.")
        return self.data.get('value')[0].get(str(key))

    async def delete(self, key: int) -> None:
        if str(key) not in self.data.get("value")[0].keys():
            raise NotFoundError('Такого ключа не найдено.')
        self.data.get('value')[0].pop(str(key))