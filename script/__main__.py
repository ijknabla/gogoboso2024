from __future__ import annotations

from pathlib import Path

import click
from polars import Datetime, String, UInt32, col, read_csv


@click.command()
@click.option("--log-csv", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(log_csv: Path | None = None) -> None:
    if log_csv is None:
        log_csv = Path(__file__, "../log.csv").resolve()

    log = read_csv(log_csv).with_columns(
        col("id").cast(UInt32),
        col("time").cast(Datetime(time_unit="ms")).dt.replace_time_zone("Asia/Tokyo"),
        col("title").cast(String),
    )

    log.write_csv(log_csv, include_bom=True)


if __name__ == "__main__":
    main()
