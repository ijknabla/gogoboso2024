from asyncio import run
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps
from typing import Protocol, TypeVar

import click
import pyppeteer

ROOT_URI = "https://platinumaps.jp/d/gogoboso2024"


@click.command()
@click.option("--headless/--headful", default=True)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def main(
    *,
    headless: bool,
) -> None:
    async with _closing(
        await pyppeteer.launch(args=["--lang=ja"], headless=headless)
    ) as browser:
        (page,) = await browser.pages()
        await page.setExtraHTTPHeaders({"Accept-Language": "ja-JP"})
        await page.goto(ROOT_URI)
        input("Press Enter!")


class _SupportsClose(Protocol):
    async def close(self) -> None:
        pass


Closable = TypeVar("Closable", bound=_SupportsClose)


@asynccontextmanager
async def _closing(closable: Closable) -> AsyncIterator[Closable]:
    try:
        yield closable
    finally:
        await closable.close()


if __name__ == "__main__":
    main()
