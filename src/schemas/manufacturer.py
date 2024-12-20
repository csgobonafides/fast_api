from pydantic import BaseModel


class ManufacturerRequest(BaseModel):
    manufacturer: str
    country: str


class ManufacturerResponse(BaseModel):
    id: str
    manufacturer: str
    country: str
