import uuid

from fastapi import APIRouter, Depends, status
from schemas.manufacturer import ManufacturerRequest, ManufacturerResponse
from controllers.manufacturer import get_controller, ManufacturerController

router = APIRouter()


@router.post("/", response_model=ManufacturerResponse, status_code=status.HTTP_201_CREATED)
async def create_manufacturer(lamp: ManufacturerRequest,
                              controller: ManufacturerController = Depends(get_controller)) -> ManufacturerResponse:
    return await controller.add_manufacturer(lamp)


@router.get('/', response_model=list[ManufacturerResponse])
async def get_manufacturer_list(controller: ManufacturerController = Depends(get_controller)) \
        -> list[ManufacturerResponse]:
    return await controller.get_all_manufacturer()


@router.get('/{manufacturer_id}', response_model=ManufacturerResponse)
async def get_by_id(manufacturer_id: uuid.UUID, controller: ManufacturerController = Depends(get_controller)) -> ManufacturerResponse:
    return await controller.get_by_id(manufacturer_id)


@router.delete('/{manufacturer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(manufacturer_id: uuid.UUID,
                       controller: ManufacturerController = Depends(get_controller)) -> None:
    await controller.del_by_id(manufacturer_id)
    return
