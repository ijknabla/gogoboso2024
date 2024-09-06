from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

from sqlalchemy import Engine, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from . import types  # noqa: TCH001

if TYPE_CHECKING:
    from dataclasses import dataclass as _check_argument

else:

    def _check_argument(x: object) -> object:
        return x


@cache
def create_engine() -> Engine:
    from sqlalchemy import create_engine

    path = Path(__file__) / "../gobo2024.sqlite"
    return create_engine(f"sqlite:///{path.resolve()}")


class Table(DeclarativeBase):
    pass


@_check_argument
class SpotTitle(Table):
    __tablename__ = "spot.title"

    id: Mapped[types.SpotId] = mapped_column(Integer(), primary_key=True)
    text: Mapped[str] = mapped_column(String())


@_check_argument
class SpotStamp(Table):
    __tablename__ = "spot.stamp"

    id: Mapped[types.SpotId] = mapped_column(Integer(), primary_key=True)
    stamp_id: Mapped[types.StampId] = mapped_column(Integer())


@_check_argument
class SpotLocation(Table):
    __tablename__ = "spot.location"

    id: Mapped[types.SpotId] = mapped_column(Integer(), primary_key=True)
    longitude: Mapped[types.Longitude] = mapped_column(Float())
    latitude: Mapped[types.Latitude] = mapped_column(Float())


@_check_argument
class StampType(Table):
    __tablename__ = "stamp.type"

    id: Mapped[types.StampId] = mapped_column(Integer(), primary_key=True)
    text: Mapped[types.StampType] = mapped_column(String())
