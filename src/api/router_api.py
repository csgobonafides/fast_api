from fastapi import APIRouter
from src.schemas.items import Item


router_api = APIRouter()


@router_api.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return item


@router_api.get("/items/", response_model=list[Item])
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
        ]