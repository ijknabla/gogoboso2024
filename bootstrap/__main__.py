from __future__ import annotations

import re
import sys
from asyncio import run
from contextlib import asynccontextmanager
from functools import wraps
from json import dump, loads
from typing import IO, TYPE_CHECKING, Protocol, TypeVar

import click
import pyppeteer

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

ROOT_URI = "https://platinumaps.jp/d/gogoboso2024"
MAPS_URI = "https://platinumaps.jp/maps/gogoboso2024"
LIST_URI = f"{MAPS_URI}?list=1"


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
    async with _closing(
        await pyppeteer.launch(args=["--lang=ja"], headless=headless)
    ) as browser:
        (page,) = await browser.pages()
        await page.setExtraHTTPHeaders({"Accept-Language": "ja-JP"})
        await page.goto(LIST_URI)
        window_bootoption = "window.__bootOptions"
        boot_options_xpath = f"//script[starts-with(.,{window_bootoption!r})]"
        await page.waitForXPath(boot_options_xpath)
        for script in await page.Jx(boot_options_xpath):
            source = await (await script.getProperty("textContent")).jsonValue()
            matched = re.match(
                rf"^{re.escape(window_bootoption)}\s+=\s+(?P<json>\{{.*\}});$", source
            )
            if matched is None:
                raise ValueError(source)
            data = loads(matched.group("json"))
            dump(data, output, indent=indent)


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
