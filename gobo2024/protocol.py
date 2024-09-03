from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def closing(closable: Closable) -> AsyncIterator[Closable]:
    try:
        yield closable
    finally:
        await closable.close()


class SupportsClose(Protocol):
    async def close(self) -> None:
        pass


Closable = TypeVar("Closable", bound=SupportsClose)
