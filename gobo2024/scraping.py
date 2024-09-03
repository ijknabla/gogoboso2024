from __future__ import annotations

import json
import re
from contextlib import AsyncExitStack, asynccontextmanager
from typing import TYPE_CHECKING, Any

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


async def scrape_boot_options(
    page: Page,
    *,
    uri: str = "https://platinumaps.jp/maps/gogoboso2024?list=1",
    target: str = "window.__bootOptions",
) -> Any:  # noqa: ANN401
    await page.goto(uri)

    xpath = f"//script[starts-with(.,{target!r})]"
    await page.waitForXPath(xpath)
    for element in await page.Jx(xpath):
        text = await (await element.getProperty("textContent")).jsonValue()
        matched = re.match(f"^{re.escape(target)}" r"\s+=\s+(?P<json>\{.*\});$", text)
        if matched is None:
            raise RuntimeError(text)

        return json.loads(matched.group("json"))

    raise RuntimeError
