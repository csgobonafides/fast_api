from fastapi import APIRouter, Depends, status
from schemas.lamp import LampIN, LampDtlInfo
from schemas.enums import SortOrder, FilterType, DetailType
from controllers.lamp import get_controller, LampController

router = APIRouter()


@router.post("/", response_model=LampDtlInfo, status_code=status.HTTP_201_CREATED)
async def create_lamp(lamp: LampIN, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.add_lamp(lamp)


@router.get('/', response_model=list[LampDtlInfo])
async def get_lamp_list(sort: SortOrder = SortOrder.desc,
                        filters: FilterType = None,
                        detail: DetailType = None,
                        controller: LampController = Depends(get_controller)) -> list[LampDtlInfo]:
    return await controller.get_all(sort, filters, detail)


@router.get('/{lamp_article}', response_model=LampDtlInfo)
async def get_by_id(lamp_article: int, controller: LampController = Depends(get_controller)) -> LampDtlInfo:
    return await controller.get_by_article(lamp_article)


@router.delete('/{lamp_article}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(lamp_article: int, controller: LampController = Depends(get_controller)) -> None:
    await controller.del_by_article(lamp_article)
    return
