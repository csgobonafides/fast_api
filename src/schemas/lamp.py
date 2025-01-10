from pydantic import BaseModel, UUID4
from schemas.manufacturer import ManufacturerResponse
from schemas.enums import ShapeType, BaseType, TemperatureType


class LampBase(BaseModel):
    price: float
    article: int


class LampIN(LampBase):
    shape: ShapeType
    base: BaseType
    temperature: TemperatureType
    manufacturer_id: UUID4


class LampOUT(LampBase):
    id: UUID4
    country: str


class LampDtlInfo(LampBase):
    id: UUID4
    shape: ShapeType
    base: BaseType
    temperature: TemperatureType
    create_at: str
    manufacturer: ManufacturerResponse
