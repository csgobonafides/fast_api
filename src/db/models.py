from datetime import timezone
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, UUID, String, DateTime, func, INT, ForeignKey

Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(UUID, primary_key=True)
    manufacturer = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)
    create_at = Column(DateTime, server_default=func.now(tz=timezone.utc))


class Lamp(Base):
    __tablename__ = "Lamps"
    id = Column(UUID, primary_key=True)
    article = Column(UUID, nullable=False)
    price = Column(INT, nullable=False)
    shape = Column(String(5), nullable=False)
    base = Column(String(5), nullable=False)
    temperature = Column(String(2), nullable=False)
    fk_lamps_manufacturers = Column(ForeignKey(Manufacturer.id), nullable=False)
    create_at = Column(DateTime, server_default=func.now(tz=timezone.utc))
