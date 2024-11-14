from fastapi import APIRouter
from src.schemas.items import Item
import logging


router = APIRouter()
logger = logging.getLogger('items_router')


@router.post("/{items}")
async def create_item(item: Item) -> Item:
    return item


@router.get("/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
        ]

@router.get('/exceptions')
async def exceptions():
    return 2 / 0