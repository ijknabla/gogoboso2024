from __future__ import annotations

import re
from asyncio import gather
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from pyppeteer import launch

from gobo2024.types import Address, BootOptions, SpotDetail, SpotId

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Awaitable, Callable

    from pyppeteer.page import Page


URI = "https://platinumaps.jp/d/gogoboso2024"


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
    uri: str = URI,
    target: str = "window.__bootOptions",
) -> BootOptions:
    return await _find_boot_options(
        page,
        uri=await _find_iframe_src(page, uri=uri),
        target=target,
    )


async def _find_boot_options(page: Page, uri: str, target: str) -> BootOptions:
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


async def scrape_spot_detail(
    page: Page, spot_id: SpotId, *, uri: str = URI
) -> SpotDetail:
    return await _find_spot_detail(
        page, uri=await _find_iframe_src(page, uri + f"?spot={spot_id}")
    )


async def _find_spot_detail(page: Page, uri: str) -> SpotDetail:
    await page.goto(uri)

    subtitle: str | BaseException | None
    title, subtitle, description, address = await gather(
        _find_text_by_xpath(page, '//div[@class="detail__title"]'),
        _find_text_by_xpath(page, '//div[@class="detail__subtitletext"]'),
        _find_text_by_xpath(page, '//div[@class="ptmdescription__text"]'),
        _find_text_by_xpath(page, "//address"),
        return_exceptions=True,
    )

    if isinstance(title, BaseException):
        raise title
    if isinstance(subtitle, BaseException):
        subtitle = None
    if isinstance(description, BaseException):
        raise description
    if isinstance(address, BaseException):
        raise address

    return SpotDetail(
        title=title,
        subtitle=subtitle,
        description=description,
        address=Address(address),
    )


async def _find_iframe_src(page: Page, uri: str) -> str:
    xpath = "//iframe"
    await page.goto(uri)
    await page.waitForXPath(xpath)
    for element in await page.Jx(xpath):
        map_uri: str = await (await element.getProperty("src")).jsonValue()
        return map_uri

    raise RuntimeError


async def _find_text_by_xpath(page: Page, xpath: str) -> str:
    await page.waitForXPath(xpath)
    for element in await page.Jx(xpath):
        text: str = await (await element.getProperty("textContent")).jsonValue()
        return text
    raise RuntimeError
