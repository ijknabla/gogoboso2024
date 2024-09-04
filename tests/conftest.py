from __future__ import annotations

from typing import TYPE_CHECKING

import pytest_asyncio

from gobo2024.scraping import open_page, scrape_boot_options

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pyppeteer.page import Page

    from gobo2024.types import BootOptions


@pytest_asyncio.fixture
async def page() -> AsyncIterator[Page]:
    async with open_page(headless=True) as page:
        yield page


@pytest_asyncio.fixture
async def boot_options(page: Page) -> BootOptions:
    return await scrape_boot_options(page)
