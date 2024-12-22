from datetime import timezone
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, UUID, String, DateTime, func, INT, ForeignKey, DECIMAL

Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id = Column(UUID, primary_key=True)
    manufacturer = Column(String(20), unique=True, nullable=False)
    country = Column(String(20), nullable=False)
    create_at = Column(DateTime, server_default=func.now(tz=timezone.utc))


class Lamp(Base):
    __tablename__ = "lamp"
    id = Column(UUID, primary_key=True)
    article = Column(INT, unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    shape = Column(String(10), nullable=False)
    base = Column(String(10), nullable=False)
    temperature = Column(String(10), nullable=False)
    manufacturer_id = Column(ForeignKey(Manufacturer.id), nullable=False)
    create_at = Column(DateTime, server_default=func.now(tz=timezone.utc))
