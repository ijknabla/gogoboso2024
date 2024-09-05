from pathlib import Path

from sqlalchemy import create_engine

from gobo2024.db import Table


def main() -> None:
    path = (Path(__file__) / "../gobo2024/gobo2024.db").resolve()
    engine = create_engine(f"sqlite:///{path}")

    # CREATE TABLE
    Table.metadata.create_all(engine)


if __name__ == "__main__":
    main()
