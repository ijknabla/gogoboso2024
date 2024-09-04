from __future__ import annotations

import csv
import sys
from asyncio import run
from functools import wraps
from typing import IO

import click

from .scraping import open_page, scrape_boot_options


@click.group()
def main() -> None: ...


@main.command
@click.option(
    "-o", "--output", type=click.File("w", encoding="utf-8"), default=sys.stdout
)
@click.option("--indent", type=int)
@click.option("--headless/--headful", default=True)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def boot_options(
    *,
    output: IO[str],
    indent: int | None,
    headless: bool,
) -> None:
    async with open_page(headless=headless) as page:
        boot_options = await scrape_boot_options(page)
        print(boot_options.model_dump_json(indent=indent), file=output)


@main.command
@click.option(
    "-o", "--output", type=click.File("w", encoding="utf-8-sig"), default=sys.stdout
)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def googlemap(
    *,
    output: IO[str],
) -> None:
    async with open_page(headless=True) as page:
        boot_options = await scrape_boot_options(page)

    writer = csv.writer(output)

    writer.writerow(["スポット", "種類", "経度", "緯度"])
    for x in sorted(boot_options.stampRallySpots, key=lambda spot: spot.spotId):
        writer.writerow([x.spotTitle, x.stampType, x.spotLng, x.spotLat])


if __name__ == "__main__":
    main()
