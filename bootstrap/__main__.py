from asyncio import run
from functools import wraps
from importlib.resources import as_file, files

import click

from .scraping import open_new_page, scrape_boot_options


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--headless/--headful", default=True)
@click.option("--indent", type=int, default=1)
@click.option(
    "--with-event-hub-context/--without-event-hub-context",
    default=False,
)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def update(*, headless: bool, indent: int, with_event_hub_context: bool) -> None:
    async with open_new_page(headless=headless) as new_page:
        page = await new_page()
        boot_options = await scrape_boot_options(page)

    exclude = set[str]()
    if not with_event_hub_context:
        exclude.add("eventHubContext")

    with as_file(files(__package__).joinpath("resources")) as resources:
        (resources / "bootOptions.json").write_text(
            boot_options.model_dump_json(indent=indent, exclude=exclude) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
