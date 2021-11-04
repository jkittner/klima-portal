from __future__ import annotations

import contextlib
import sqlite3
from typing import Generator


@contextlib.contextmanager
def connect(db_path: str) -> Generator[sqlite3.Connection, None, None]:
    with contextlib.closing(
        sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        ),
    ) as db:
        with db:
            yield db
