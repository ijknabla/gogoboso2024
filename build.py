from pathlib import Path
from typing import cast

from sqlalchemy.orm import Session

from bootstrap import load_boot_options
from gobo2024 import db
from gobo2024.types import StampId, StampType


def main() -> None:
    engine = db.create_engine()
    if engine.url.database is not None and Path(engine.url.database).exists():
        Path(engine.url.database).unlink()

    # CREATE TABLE
    db.Table.metadata.create_all(engine)

    # load object
    boot_options = load_boot_options()

    stamp_id = {
        cast(StampType, k): StampId(v) for v, k in enumerate(["GPS", "QRCode"], start=1)
    }

    with Session(engine) as session:
        for _text, _id in stamp_id.items():
            session.add(
                db.StampType(
                    id=_id,
                    text=_text,
                )
            )

        for x in sorted(boot_options.stampRallySpots, key=lambda x: x.spotId):
            session.add(
                db.SpotTitle(
                    id=x.spotId,
                    text=x.spotTitle,
                )
            )

            session.add(db.SpotStamp(id=x.spotId, stamp_id=stamp_id[x.stampType]))

            session.add(
                db.SpotLocation(
                    id=x.spotId,
                    longitude=x.spotLng,
                    latitude=x.spotLat,
                )
            )

        session.commit()


if __name__ == "__main__":
    main()
