import json
from datetime import datetime

import pytest

from portal.api.utils import connect
from portal.api.utils import get_wind_direction
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


@pytest.mark.parametrize(
    ('strength', 'station', 'exp'),
    (
        (0.25, 1, [8, 0, 0, 0, 0, 0, 0, 0]),
        (0.5, 1, [16, 0, 8, 0, 0, 0, 0, 0]),
        (1, 1, [16, 0, 25, 0, 0, 0, 0, 0]),
        (0.5, 12, [0, 0, 33, 0, 0, 0, 16, 0]),
    ),
)
def test_get_wind_direction(strength, station, exp):
    wind = get_wind_direction(strength, station=station)
    assert wind == exp


def test_data(client):
    resp = client.get('/api/data?param=lufttemp_5&station=1')
    data = resp.data.decode()
    data_parsed = json.loads(data)
    assert resp.status_code == 200
    assert data_parsed == {
        'x': [
            '2021-05-30T17:00:00', '2021-05-30T20:00:00',
            '2021-05-30T23:00:00', '2021-05-31T02:00:00',
            '2021-05-31T05:03:00', '2021-05-31T08:33:00',
            '2021-05-31T11:15:00', '2021-05-31T14:01:00',
        ],
        'y': [24.0, 22.5, 18.4, 14.9, 13.1, 20.5, 25.6, 25.9],
        'name': 'Lufttemperatur 0,05 m',
        'unit': 'Temperatur [°C]',
        'type': 'scatter',
    }


def test_data_unknown_parameter(client):
    resp = client.get('/api/data?param=unknown&station=1')
    data = resp.data.decode()
    data_parsed = json.loads(data)
    assert resp.status_code == 400
    assert data_parsed == {
        'code': 400,
        'message': 'unknown param',
    }


def test_wind_data(client):
    resp = client.get('/api/data/wind?station=1')
    data = resp.data.decode()
    data_parsed = json.loads(data)
    assert resp.status_code == 200
    assert data_parsed == [
        {
            'marker': {'color': '#9e0142'},
            'name': '> 1 m/s',
            'r': [25, 0, 33, 0, 0, 0, 0, 0],
            'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
            'type': 'barpolar',
        },
        {
            'marker': {'color': '#fa8c4e'},
            'name': '< 1 m/s',
            'r': [16, 0, 25, 0, 0, 0, 0, 0],
            'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
            'type': 'barpolar',
        },
        {
            'marker': {'color': '#ffffbf'},
            'name': '< 0,75 m/s',
            'r': [16, 0, 8, 0, 0, 0, 0, 0],
            'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
            'type': 'barpolar',
        },
        {
            'marker': {'color': '#88d1a4'},
            'name': '< 0,5 m/s',
            'r': [16, 0, 8, 0, 0, 0, 0, 0],
            'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
            'type': 'barpolar',
        },
        {
            'marker': {'color': '#5e4fa2'},
            'name': '< 0,25 m/s',
            'r': [8, 0, 0, 0, 0, 0, 0, 0],
            'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
            'type': 'barpolar',
        },
    ]
