import sqlite3
from pathlib import Path


def main() -> None:
    db = (Path(__file__) / "../gobo2024/gobo2024.db").resolve()

    connection = sqlite3.connect(db)
    connection.close()


if __name__ == "__main__":
    main()
