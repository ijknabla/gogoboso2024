from asyncio import run
from functools import wraps

import click
import pyppeteer


@click.command()
@click.option("--headless/--headful", default=True)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def main(
    *,
    headless: bool,
) -> None:
    browser = await pyppeteer.launch(headless=headless)
    await browser.close()


if __name__ == "__main__":
    main()
