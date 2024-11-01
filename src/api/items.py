from fastapi import APIRouter
from src.schemas.items import Item


router = APIRouter()


@router.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@router.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
        ]