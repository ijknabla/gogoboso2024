from __future__ import annotations

import logging
from asyncio import CancelledError, create_task, gather, run, wait
from asyncio.queues import Queue
from collections import ChainMap
from contextlib import suppress
from functools import wraps
from importlib.resources import as_file, files
from typing import TYPE_CHECKING

import click
from pydantic import RootModel

from gobo2024.types import SpotDetail, SpotId

from .scraping import open_new_page, scrape_boot_options, scrape_spot_detail

if TYPE_CHECKING:
    from pyppeteer.page import Page


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--headless/--headful", default=True)
@click.option("-n", type=int, default=0)
@click.option("-v", "--verbose", count=True)
@click.option("--indent", type=int, default=1)
@click.option(
    "--with-event-hub-context/--without-event-hub-context",
    default=False,
)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def update(
    *, headless: bool, n: int, verbose: int, indent: int, with_event_hub_context: bool
) -> None:
    if verbose > 0:
        logging.root.addHandler(logging.StreamHandler())
        logging.root.setLevel({1: logging.INFO}.get(verbose, logging.DEBUG))
    async with open_new_page(headless=headless) as new_page:
        page = await new_page()
        boot_options = await scrape_boot_options(page)

        spots = Queue[SpotId]()
        for x in boot_options.stampRallySpots:
            await spots.put(x.spotId)

        pages = [page]
        for _ in range(n - 1):
            pages.append(await new_page())  # noqa: PERF401

        spot_detail = RootModel[dict[SpotId, SpotDetail]](
            dict(
                sorted(
                    ChainMap(
                        *await gather(
                            *(
                                _scrape_spot_detail(page, spots)
                                for rank, page in enumerate(pages)
                            )
                        )
                    ).items()
                )
            )
        )

    exclude = set[str]()
    if not with_event_hub_context:
        exclude.add("eventHubContext")

    with as_file(files(__package__).joinpath("resources")) as resources:
        (resources / "bootOptions.json").write_text(
            boot_options.model_dump_json(indent=indent, exclude=exclude) + "\n",
            encoding="utf-8",
        )

        (resources / "spot_detail.json").write_text(
            spot_detail.model_dump_json(indent=indent) + "\n", encoding="utf-8"
        )


async def _scrape_spot_detail(
    page: Page, queue: Queue[SpotId]
) -> dict[SpotId, SpotDetail]:
    result = dict[SpotId, SpotDetail]()

    queue_join = create_task(queue.join())

    while True:
        queue_get = create_task(queue.get())

        done, pending = await wait(
            {queue_join, queue_get}, return_when="FIRST_COMPLETED"
        )

        if queue_get in done:
            queue.task_done()
            spot_id = queue_get.result()
            result[spot_id] = await scrape_spot_detail(page, spot_id=spot_id)
        else:
            for task in pending:
                task.cancel()
            for task in pending:
                with suppress(CancelledError):
                    await task
            break

    return result


if __name__ == "__main__":
    main()
