from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gobo2024.types import BootOptions


def test_boot_options(boot_options: BootOptions) -> None:
    spots = boot_options.stampRallySpots

    assert set(Counter(spot.id for spot in spots).values()) == {1}

    for spot in spots:
        assert spot.stampType == spot.stampTypeText
