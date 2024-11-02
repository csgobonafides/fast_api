from fastapi import APIRouter
from src.schemas.items import Item


router = APIRouter()


@router.post("/items")
async def create_item():
    return


@router.get("/items")
async def read_items():
    return