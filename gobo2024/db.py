from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from . import types


class Table(DeclarativeBase):
    pass


class SpotTitle(Table):
    __tablename__ = "spot.title"

    id: Mapped[types.SpotId] = mapped_column(Integer(), primary_key=True)
    text: Mapped[str] = mapped_column(String())


class SpotLocation(Table):
    __tablename__ = "spot.location"

    id: Mapped[types.SpotId] = mapped_column(Integer(), primary_key=True)
    longitude: Mapped[types.Longitude] = mapped_column(Float())
    latitude: Mapped[types.Latitude] = mapped_column(Float())


class StampType(Table):
    __tablename__ = "stamp.type"

    id: Mapped[types.StampId] = mapped_column(Integer(), primary_key=True)
    text: Mapped[types.StampType] = mapped_column(String())
