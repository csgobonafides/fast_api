from fastapi import APIRouter, Depends, Request, Response
from src.schemas.lamps import LampIN, LampOUT, LampDtlInfo
from src.controllers.work_to_db import get_controller
import logging


router = APIRouter()
logger = logging.getLogger('items_router')


@router.post("/add_lamp")
async def add_lamp(lamp: LampIN, controller = Depends(get_controller)) -> LampIN:
    return await controller.add_lamp(lamp)


@router.get('/get_all')
async def get_all(controller = Depends(get_controller)) -> list[LampOUT]:
    return await controller.get_all()


@router.post('/get_by_id')
async def get_by_id(id: int, controller = Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_id(id)


@router.delete('/del_by_id')
async def del_by_id(id: int, controller = Depends(get_controller)):
    return await controller.del_by_id(id)




# @router.get("/")
# async def read_items() -> list[Item]:
#     return [
#         Item(name="Portal Gun", price=42.0),
#         Item(name="Plumbus", price=32.0),
#         ]