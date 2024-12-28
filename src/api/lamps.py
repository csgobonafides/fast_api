from typing import Literal
from fastapi import APIRouter, Depends, status
from schemas.lamp import LampIN, LampOUT, LampDtlInfo
from controllers.lamp import get_controller, LampController

router = APIRouter()


@router.post("/", response_model=LampDtlInfo, status_code=status.HTTP_201_CREATED)
async def create_lamp(lamp: LampIN, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.add_lamp(lamp)


@router.get('/', response_model=list[LampDtlInfo])
async def get_lamp_list(sort: Literal['asc', 'desc'] = "desc",
                        filter: Literal['shape', 'base', 'temperature'] = None,
                        detail: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63',
                        'E40', 'E27', 'E14',
                        'ww', 'nw', 'cw'] = None,
                        controller: LampController = Depends(get_controller)) -> list[LampDtlInfo]:
    return await controller.get_all(sort, filter, detail)


@router.get('/{lamp_article}', response_model=LampDtlInfo)
async def get_by_id(lamp_article: int, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_article(lamp_article)


@router.delete('/{lamp_article}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lamp_article: int, controller: LampController = Depends(get_controller)) -> None:
    await controller.del_by_article(lamp_article)
    return
