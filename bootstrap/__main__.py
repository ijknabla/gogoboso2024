from asyncio import run
from functools import wraps
from importlib.resources import as_file, files

import click

from gobo2024.scraping import open_page, scrape_boot_options


@click.group()
def main() -> None:
    pass


@main.command()
@click.option("--headless/--headful", default=True)
@click.option("--indent", type=int, default=1)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def update(*, headless: bool, indent: int) -> None:
    async with open_page(headless=headless) as page:
        boot_options = await scrape_boot_options(page)

    with as_file(files(__package__).joinpath("resources")) as resources:
        (resources / "bootOptions.json").write_text(
            boot_options.model_dump_json(indent=indent), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
