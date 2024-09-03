from asyncio import run
from functools import wraps

import click


@click.command()
@(lambda f: wraps(f)(lambda *args, **kwargs: run(f(*args, **kwargs))))
async def main() -> None:
    pass


if __name__ == "__main__":
    main()
