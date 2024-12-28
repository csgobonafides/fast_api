from typing import Literal
from pydantic import BaseModel, UUID4


class LampBase(BaseModel):
    price: float
    article: int


class LampIN(LampBase):
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal['E40', 'E27', 'E14']
    temperature: Literal['ww', 'nw', 'cw']
    manufacturer_id: str


class LampOUT(LampBase):
    id: UUID4
    name: str
    country: str


class LampDtlInfo(LampBase):
    id: UUID4
    name: str
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal["E40", "E27", "E14"]
    temperature: Literal['ww', 'nw', 'cw']
    create_at: str
    country: str
