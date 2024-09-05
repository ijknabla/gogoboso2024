from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from bootstrap import load_boot_options
from gobo2024.db import SpotLocation, SpotTitle, Table


def main() -> None:
    path = (Path(__file__) / "../gobo2024/gobo2024.sqlite").resolve()
    engine = create_engine(f"sqlite:///{path}")

    # CREATE TABLE
    Table.metadata.create_all(engine)

    # load object
    boot_options = load_boot_options()

    with Session(engine) as session:
        for x in sorted(boot_options.stampRallySpots, key=lambda x: x.spotId):
            session.add(
                SpotTitle(
                    id=x.spotId,
                    text=x.spotTitle,
                )
            )

            session.add(
                SpotLocation(
                    id=x.spotId,
                    longitude=x.spotLng,
                    latitude=x.spotLat,
                )
            )

        session.commit()


if __name__ == "__main__":
    main()
