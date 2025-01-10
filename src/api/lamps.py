from fastapi import APIRouter, Depends, status
from schemas.lamp import LampIN, LampDtlInfo
from schemas.enums import SortOrder, FilterType, ShapeType, BaseType, TemperatureType
from controllers.lamp import get_controller, LampController
import uuid

router = APIRouter()


@router.post("/", response_model=LampDtlInfo, status_code=status.HTTP_201_CREATED)
async def create_lamp(lamp: LampIN, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.add_lamp(lamp)


@router.get('/', response_model=list[LampDtlInfo])
async def get_lamp_list(sort: SortOrder = SortOrder.desc,
                        shape: list[ShapeType] = None,
                        base: list[BaseType] = None,
                        temperature: list[TemperatureType] = None,
                        controller: LampController = Depends(get_controller)) -> list[LampDtlInfo]:
    return await controller.get_all(sort, shape, base, temperature)


@router.get('/{lamp_id}', response_model=LampDtlInfo)
async def get_by_id(lamp_id: uuid.UUID, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_id(lamp_id)


@router.delete('/{lamp_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lamp_id: uuid.UUID, controller: LampController = Depends(get_controller)) -> None:
    await controller.del_by_id(lamp_id)
    return
