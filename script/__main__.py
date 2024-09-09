from __future__ import annotations

from pathlib import Path

import click
from polars import DataType, Datetime, String, UInt32, col, read_csv


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

    log = read_csv(log_csv, schema=dtypes).with_columns(
        col("time").dt.convert_time_zone("Asia/Tokyo"),
    )

    log.write_csv(log_csv, include_bom=True)


if __name__ == "__main__":
    main()
