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


def get_wind_direction(strength_class: int | float, station: int) -> list[int]:
    with connect('app.db') as db:
        ret = db.execute(
            '''\
            SELECT
                windrichtung, (count(windrichtung) * 100 / 12)
            FROM measurements
            WHERE
                station = ?
                AND windrichtung IS NOT NULL
                AND windgeschw_200 < ?
            GROUP BY windrichtung;
            ''',
            (station, strength_class),
        ).fetchall()
    wind_dirs = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
    wind_dict = {k: 0 for k in wind_dirs}
    for r in ret:
        wind_dict[r[0]] = r[1]

    return list(wind_dict.values())
