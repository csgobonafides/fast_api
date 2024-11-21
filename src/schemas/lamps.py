from typing import Union, Literal
from pydantic import BaseModel


class LampBase(BaseModel):
    name: str
    price: float


class LampIN(LampBase):
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal["E40", "E27", "E14"]
    temperature: Literal['ww', 'nw', 'cw']

class LampOUT(LampBase):
    id: str

class LampDtlInfo(LampBase):
    id: str
    shape: Literal['A60', 'C37', 'G45', 'R39', 'R50', 'R63']
    base: Literal["E40", "E27", "E14"]
    temperature: Literal['ww', 'nw', 'cw']