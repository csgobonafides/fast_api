import json
from storages.base import CacheStorage
from core.exceptions import NotFoundError, BadRequestError


class JsonFileStorage(CacheStorage):
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.data = {}

    async def connect(self) -> None:
        if self.file_path is None:
            return

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    async def disconnect(self) -> None:
        if self.file_path is None:
            return
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)

    async def add(self, key: str, value: dict) -> None:
        if key in self.data:
            raise BadRequestError("Such a key already exists.")
        self.data[key] = value

    async def get_all(self) -> list[dict]:
        return list(self.data.values())

    async def get(self, key: str) -> dict:
        if key not in self.data:
            raise NotFoundError
        return self.data.get(key)

    async def delete(self, key: str) -> None:
        if key not in self.data:
            raise NotFoundError
        self.data.pop(key)
        if key not in self.data:
            return
