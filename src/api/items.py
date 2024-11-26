from fastapi import APIRouter, Depends, Request, Response, status
from schemas.lamps import LampIN, LampOUT, LampDtlInfo
from controllers.work_to_db import get_controller
import logging

router = APIRouter()
logger = logging.getLogger('items_router')


@router.post("/add_lamp")
async def add_lamp(lamp: LampIN, controller=Depends(get_controller)) -> LampIN:
    return await controller.add_lamp(lamp)


@router.get('/get_all')
async def get_all(controller=Depends(get_controller)) -> list[LampOUT]:
    return await controller.get_all()


@router.get('/{lamp_id}')
async def get_by_id(lamp_id: str, controller=Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_id(lamp_id)


@router.delete('/{lamp_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_by_id(lamp_id: str, controller=Depends(get_controller)):
    return await controller.del_by_id(lamp_id)