from datetime import datetime

from portal.api.utils import connect
from portal.app import app


def test_database_can_query():
    with connect(app.config['DB_PATH']) as db:
        result = db.execute(
            # sqlite needs this type casting to return a proper datetime object
            '''\
            SELECT datum as "[timestamp]", lufttemp_200
            FROM measurements
            WHERE station = 1 AND datum BETWEEN ? AND ?
            ''',
            (datetime(2021, 5, 30, 23, 0, 0), datetime(2021, 5, 31, 3, 0, 0)),
        ).fetchall()
    assert result == [
        (datetime(2021, 5, 30, 23, 0), 18.1),
        (datetime(2021, 5, 31, 2, 0), 14.6),
    ]
