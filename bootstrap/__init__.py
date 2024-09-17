import json
from contextlib import ExitStack
from functools import cache
from importlib.resources import as_file, files

from gobo2024.types import BootOptions


@cache
def load_boot_options() -> BootOptions:
    with ExitStack() as stack:
        enter = stack.enter_context

        boot_options_path = enter(
            as_file(files(__package__).joinpath("resources/bootOptions.json"))
        )
        boot_options_io = enter(boot_options_path.open("r", encoding="utf-8"))
        return BootOptions.model_validate(json.load(boot_options_io))

    raise NotImplementedError
