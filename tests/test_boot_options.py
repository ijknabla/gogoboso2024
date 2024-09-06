from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

from gobo2024 import db
from gobo2024.types import StampRallySpot

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from gobo2024.types import BootOptions


def test_boot_options(session: Session, boot_options: BootOptions) -> None:
    spots = boot_options.stampRallySpots

    assert set(Counter(spot.id for spot in spots).values()) == {1}
    assert set(Counter(spot.spotId for spot in spots).values()) == {1}

    for spot in spots:
        spot_title = (
            session.query(db.SpotTitle).filter(db.SpotTitle.id == spot.spotId).first()
        )
        assert spot_title is not None

        stamp_id = (
            session.query(db.SpotStamp.stamp_id)
            .filter(db.SpotStamp.id == spot.spotId)
            .scalar_subquery()
        )
        stamp_type = (
            session.query(db.StampType).filter(db.StampType.id == stamp_id).first()
        )
        assert stamp_type is not None

        spot_location = (
            session.query(db.SpotLocation)
            .filter(db.SpotLocation.id == spot.spotId)
            .first()
        )
        assert spot_location is not None

        assert spot == StampRallySpot(
            checkinPoints=spot.checkinPoints,  # TODO: use database
            spotId=spot.spotId,
            spotTitle=spot_title.text,
            stampType=stamp_type.text,
            stampTypeText=stamp_type.text,
            spotLng=spot_location.longitude,
            spotLat=spot_location.latitude,
            id=spot.id,  # NOTE: arbitary value
            stampRallyIcon=spot.stampRallyIcon,  # NOTE: arbitary value
        )
