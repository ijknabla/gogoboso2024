from __future__ import annotations

from pathlib import Path

import click
from polars import DataFrame, DataType, Datetime, String, UInt32, col, read_csv
from sqlalchemy.orm import Session

from gobo2024 import db


@click.command()
@click.option("--log-csv", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(log_csv: Path | None = None) -> None:
    if log_csv is None:
        log_csv = Path(__file__, "../log.csv").resolve()

    dtypes: dict[str, DataType | type[DataType]] = {
        "id": UInt32,
        "time": Datetime(time_unit="ms"),
        "title": String,
    }

    log = (
        read_csv(log_csv, schema=dtypes)
        .with_columns(
            col("time").dt.convert_time_zone("Asia/Tokyo"),
        )
        .with_row_index(name="row", offset=2)
    )

    with Session(db.create_engine()) as s:
        spot_titles = []

        for row, id_in_csv, title_in_csv in log.select(
            "row", "id", "title"
        ).iter_rows():
            if (
                by_id := s.query(db.SpotTitle)
                .filter(db.SpotTitle.id == id_in_csv)
                .all()
            ):
                (spot_title,) = by_id
            elif (
                by_title := s.query(db.SpotTitle)
                .filter(db.SpotTitle.text.contains(title_in_csv))
                .all()
            ):
                spot_title, *rest = by_title
                if rest:
                    candidates = sorted(x.text for x in by_title)
                    message = (
                        f"{row=!r}: "
                        f"Ambiguous spot title {title_in_csv!r} in {candidates!r}"
                    )
                    raise ValueError(message)
            else:
                message = f"{row=!r}: {id_in_csv=!r}, {title_in_csv=!r}"
                raise ValueError(message)

            spot_titles.append(spot_title)

        log = log.update(
            DataFrame(
                {
                    "id": [x.id for x in spot_titles],
                    "title": [x.text for x in spot_titles],
                }
            )
        )
    log.select(*dtypes).write_csv(log_csv, include_bom=True)


if __name__ == "__main__":
    main()
