from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
from typing import TYPE_CHECKING

from pyppeteer import launch

from .protocol import closing

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pyppeteer.page import Page


@asynccontextmanager
async def open_page(*, headless: bool) -> AsyncIterator[Page]:
    async with AsyncExitStack() as stack:
        enter = stack.enter_async_context

        browser = await enter(
            closing(await launch(args=["--lang=ja"], headless=headless))
        )
        for page in await browser.pages():
            await enter(closing(page))
            await page.setExtraHTTPHeaders({"Accept-Language": "ja-JP"})
            yield page
            return
