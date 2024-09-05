from sqlalchemy import Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .types import Latitude, Longitude, SpotId


class Table(DeclarativeBase):
    pass


class SpotLocation(Table):
    __tablename__ = "spot.location"

    id: Mapped[SpotId] = mapped_column(Integer(), primary_key=True)
    longitude: Mapped[Longitude] = mapped_column(Float())
    latitude: Mapped[Latitude] = mapped_column(Float())
