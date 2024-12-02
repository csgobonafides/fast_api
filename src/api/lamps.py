from fastapi import APIRouter, Depends, status
from schemas.lamps import LampIN, LampOUT, LampDtlInfo
from controllers.lamps_controller import get_controller

router = APIRouter()


@router.post("/", response_model=LampDtlInfo, status_code=status.HTTP_201_CREATED)
async def create_lamp(lamp: LampIN, controller=Depends(get_controller)) -> LampDtlInfo:
    return await controller.add_lamp(lamp)


@router.get('/', response_model=list[LampOUT])
async def get_lamp_list(controller=Depends(get_controller)) -> list[LampOUT]:
    return await controller.get_all()


@router.get('/{lamp_id}', response_model=LampDtlInfo)
async def get_by_id(lamp_id: str, controller=Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_id(lamp_id)


@router.delete('/{lamp_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lamp_id: str, controller=Depends(get_controller)) -> None:
    await controller.del_by_id(lamp_id)
    return