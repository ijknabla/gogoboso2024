from __future__ import annotations

import re
from asyncio import gather
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from pyppeteer import launch

from gobo2024.types import BootOptions

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Awaitable, Callable

    from pyppeteer.page import Page


@asynccontextmanager
async def open_new_page(
    *, headless: bool
) -> AsyncIterator[Callable[[], Awaitable[Page]]]:
    browser = await launch(args=["--lang=ja"], headless=headless)
    try:

        async def iterator() -> AsyncIterator[Page]:
            for page in await browser.pages():
                await page.setExtraHTTPHeaders({"Accept-Language": "ja-JP"})
                yield page
            while True:
                page = await browser.newPage()
                await page.setExtraHTTPHeaders({"Accept-Language": "ja-JP"})
                yield page

        yield iterator().__anext__

    finally:
        await gather(*(page.close() for page in await browser.pages()))
        await browser.close()


async def scrape_boot_options(
    page: Page,
    *,
    uri: str = "https://platinumaps.jp/maps/gogoboso2024?list=1",
    target: str = "window.__bootOptions",
) -> BootOptions:
    await page.goto(uri)

    xpath = f"//script[starts-with(.,{target!r})]"
    await page.waitForXPath(xpath)
    for element in await page.Jx(xpath):
        text = await (await element.getProperty("textContent")).jsonValue()
        matched = re.match(f"^{re.escape(target)}" r"\s+=\s+(?P<json>\{.*\});$", text)
        if matched is None:
            raise RuntimeError(text)

        return BootOptions.model_validate_json(matched.group("json"))

    raise RuntimeError
