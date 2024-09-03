from asyncio import run
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps
from typing import Protocol, TypeVar

import click
import pyppeteer


@click.command()
@click.option("--headless/--headful", default=True)
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def main(
    *,
    headless: bool,
) -> None:
    async with _closing(await pyppeteer.launch(headless=headless)):
        input("Press Enter!")


class SupportsClose(Protocol):
    async def close(self) -> None:
        pass


Closable = TypeVar("Closable", bound=SupportsClose)


@asynccontextmanager
async def _closing(closable: Closable) -> AsyncIterator[Closable]:
    try:
        yield closable
    finally:
        await closable.close()


if __name__ == "__main__":
    main()
