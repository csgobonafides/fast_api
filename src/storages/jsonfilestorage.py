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

    async def delete(self, key: str) -> None:
        if key not in self.data:
            raise NotFoundError('Такого ключа не найдено.')
        self.data.pop(key)
        if key not in self.data:
            return