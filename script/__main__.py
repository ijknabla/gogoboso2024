from __future__ import annotations

import csv
from pathlib import Path
from typing import IO, Any

import click
from polars import DataFrame, DataType, Datetime, String, UInt32, col, read_csv
from sqlalchemy.orm import Session

from gobo2024 import db


@click.command()
@click.option("--log-csv", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--togo", type=click.File(mode="w", encoding="utf-8-sig"))
@click.option("--done", type=click.File(mode="w", encoding="utf-8-sig"))
def main(
    log_csv: Path | None = None,
    togo: IO[str] | None = None,
    done: IO[str] | None = None,
) -> None:
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

    engine = db.create_engine()

    with Session(engine) as s:
        spot_titles = []

        for row, id_in_csv, title_in_csv in log.select(
            "row", "id", "title"
        ).iter_rows():
            if (
                by_id := s.query(db.SpotTitle)
                .filter(db.SpotTitle.id == id_in_csv)
                .all()
            ):
                (title,) = by_id
            elif title_in_csv is not None and (
                by_title := s.query(db.SpotTitle)
                .filter(db.SpotTitle.text.contains(title_in_csv))
                .all()
            ):
                title, *rest = by_title
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

            spot_titles.append(title)

        log = log.update(
            DataFrame(
                {
                    "id": [x.id for x in spot_titles],
                    "title": [x.text for x in spot_titles],
                }
            )
        )

    log.select(*dtypes).write_csv(log_csv, include_bom=True)

    if togo:
        with Session(engine) as session:
            _write_togo(csv.writer(togo), log, session)

    if done:
        with Session(engine) as session:
            _write_done(csv.writer(done), log, session)


def _write_togo(writer: Any, log: DataFrame, session: Session) -> None:
    writer.writerow(["名前", "種類", "経度", "緯度"])

    acquired = set(log["id"])
    for title in (
        session.query(db.SpotTitle).filter(db.SpotTitle.id.not_in(acquired)).all()
    ):
        stamp_id = (
            session.query(db.SpotStamp.stamp_id)
            .filter(db.SpotStamp.id == title.id)
            .scalar_subquery()
        )
        stamp_type = (
            session.query(db.StampType).filter(db.StampType.id == stamp_id).first()
        )
        if stamp_type is None:
            raise RuntimeError

        location = (
            session.query(db.SpotLocation)
            .filter(db.SpotLocation.id == title.id)
            .first()
        )
        if location is None:
            raise RuntimeError

        writer.writerow(
            [title.text, stamp_type.text, location.longitude, location.latitude]
        )


def _write_done(writer: Any, log: DataFrame, session: Session) -> None:
    writer.writerow(["通し番号", "時刻", "名前", "経度", "緯度"])

    for index, (id_, time, title) in enumerate(
        log.sort(["time", "row"], descending=[False, False], maintain_order=True)
        .select("id", "time", "title")
        .iter_rows(),
        start=1,
    ):
        location = (
            session.query(db.SpotLocation).filter(db.SpotLocation.id == id_).first()
        )
        if location is None:
            raise RuntimeError

        writer.writerow(
            [
                f"{index:0>3}",
                time.strftime("%Y年%m月%d日%H時%M分"),
                title,
                location.longitude,
                location.latitude,
            ]
        )


if __name__ == "__main__":
    main()
