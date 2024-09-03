from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gobo2024.types import BootOptions


def test_boot_options(boot_options: BootOptions) -> None:
    for spot in boot_options.stampRallySpots:
        assert not spot.useGps
        assert spot.stampType == spot.stampTypeText
