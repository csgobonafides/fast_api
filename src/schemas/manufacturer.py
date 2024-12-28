from pydantic import BaseModel, UUID4


class ManufacturerRequest(BaseModel):
    name: str
    country: str


class ManufacturerResponse(BaseModel):
    id: UUID4
    name: str
    country: str
