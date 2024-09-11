from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from sqlalchemy.orm import Session

from bootstrap.scraping import open_new_page, scrape_boot_options
from gobo2024.db import create_engine

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    from pyppeteer.page import Page

    from gobo2024.types import BootOptions


@pytest.fixture
def session() -> Iterator[Session]:
    with Session(create_engine()) as session:
        yield session


@pytest_asyncio.fixture
async def page() -> AsyncIterator[Page]:
    async with open_new_page(headless=True) as new_page:
        yield await new_page()


@pytest_asyncio.fixture
async def boot_options(page: Page) -> BootOptions:
    return await scrape_boot_options(page)
