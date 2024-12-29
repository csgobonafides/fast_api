from typing import Literal
from pydantic import BaseModel, UUID4
from schemas.manufacturer import ManufacturerResponse


class LampBase(BaseModel):
    price: float
    article: int


class LampIN(LampBase):
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal['E40', 'E27', 'E14']
    temperature: Literal['ww', 'nw', 'cw']
    manufacturer_id: UUID4


class LampOUT(LampBase):
    id: UUID4
    country: str


class LampDtlInfo(LampBase):
    id: UUID4
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal["E40", "E27", "E14"]
    temperature: Literal['ww', 'nw', 'cw']
    create_at: str
    manufacturer: ManufacturerResponse
