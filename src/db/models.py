from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, INT, ForeignKey, DECIMAL, func


class BaseModel(DeclarativeBase):
    id = Column(UUID, primary_key=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Manufacturer(BaseModel):

    __tablename__ = "manufacturer"
    name = Column(String(200), unique=True, nullable=False)
    country = Column(String(200), nullable=False)

    def __repr__(self) -> str:
        return f"Manufacturer({self.id=}, {self.name=}, {self.country=})"


class Lamp(BaseModel):

    __tablename__ = "lamp"
    article = Column(INT, unique=True, nullable=False)
    price = Column(DECIMAL(50, 2), nullable=False)
    shape = Column(String(100), nullable=False)
    base = Column(String(100), nullable=False)
    temperature = Column(String(100), nullable=False)
    manufacturer_id = Column(ForeignKey(Manufacturer.id), nullable=False)

    manufacturer = relationship(Manufacturer, backref="lamps")

    def __repr__(self) -> str:
        return (f"Lamp({self.id=}, {self.article}, {self.shape}, "
                f"{self.base}, {self.temperature}, {self.manufacturer_id})")
