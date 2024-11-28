from fastapi import APIRouter, Depends, Request, Response, status
from schemas.lamps import LampIN, LampOUT, LampDtlInfo
from controllers.work_to_db import get_controller
import logging

router = APIRouter()
logger = logging.getLogger('items_router')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_lamp(lamp: LampIN, controller=Depends(get_controller)) -> LampIN:
    return await controller.add_lamp(lamp)


@router.get('/')
async def get_lamp_list(controller=Depends(get_controller)) -> list[LampOUT]:
    return await controller.get_all()


@router.get('/{lamp_id}')
async def get_by_id(lamp_id: str, controller=Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_id(lamp_id)


@router.delete('/{lamp_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lamp_id: str, controller=Depends(get_controller)):
    return await controller.del_by_id(lamp_id)