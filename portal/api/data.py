from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

from portal.api.utils import connect
from portal.api.utils import get_wind_direction

api = Blueprint(name='api', import_name=__name__,  url_prefix='/api')


@api.route('/data')
def data() -> Response:
    columns = {
        'lufttemp_5': (1, 'Lufttemperatur 0,05 m', 'Temperatur [°C]'),
        'lufttemp_200': (2, 'Lufttemperatur 2 m', 'Temperatur [°C]'),
        'relhum': (3, 'Relative Feuchte 2 m', 'rel. Feuchte [%]'),
        'oberfl_temp_unten': (4, 'Oberfl. Temperatur unten', 'Temperatur [°C]'),  # noqa E501
        'oberfl_temp_oben': (5, 'Oberfl. Temperatur oben', 'Temperatur [°C]'),
        'oberfl_temp_links': (6, 'Oberfl. Temperatur Nord', 'Temperatur [°C]'),
        'oberfl_temp_rechts': (7, 'Oberfl. Temperatur Süd', 'Temperatur [°C]'),
        'windgeschw_5': (8, 'Windgeschwindingkeit 0,05 m', 'Windgeschwindigkeit [m/s]'),  # noqa E501
        'windgeschw_200': (9, 'Windgeschwindingkeit 2 m', 'Windgeschw. [m/s]'),
        'windrichtung': (10, 'Windrichtung', 'Windrichtung [°]'),
    }
    param = request.args['param']
    param_index = columns.get(param)
    if param_index is None:
        ret = jsonify(
            code=400,
            message='unknown param',
        )
        ret.status_code = 400
        return ret

    with connect('app.db') as db:
        ret = db.execute(
            '''\
            SELECT datum as "[timestamp]", lufttemp_5, lufttemp_200, relhum,
                oberfl_temp_unten, oberfl_temp_oben, oberfl_temp_links,
                oberfl_temp_rechts, windgeschw_5, windgeschw_200, windrichtung
            FROM measurements WHERE station = ?
            ''',
            (request.args['station'],),
        ).fetchall()

    return jsonify(
        {
            'x': [i[0].isoformat() for i in ret],
            'y': [i[param_index[0]] for i in ret],
            'name': columns[param][1],
            'unit': columns[param][2],
            'type': 'scatter',
        },
    )


@api.route('/data/wind')
def wind_data() -> Response:
    class_025 = get_wind_direction(0.25, request.args['station'])
    class_05 = get_wind_direction(0.5, request.args['station'])
    class_075 = get_wind_direction(0.75, request.args['station'])
    class_10 = get_wind_direction(1, request.args['station'])
    class_above = get_wind_direction(200, request.args['station'])
    return jsonify(
        [
            {
                'r': class_above,
                'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                'name': '> 1 m/s',
                'marker': {'color': '#9e0142'},
                'type': 'barpolar',
            },
            {
                'r': class_10,
                'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                'name': '< 1 m/s',
                'marker': {'color': '#fa8c4e'},
                'type': 'barpolar',
            },
            {
                'r': class_075,
                'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                'name': '< 0,75 m/s',
                'marker': {'color': '#ffffbf'},
                'type': 'barpolar',
            },
            {
                'r': class_05,
                'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                'name': '< 0,5 m/s',
                'marker': {'color': '#88d1a4'},
                'type': 'barpolar',
            },
            {
                'r': class_025,
                'theta': ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
                'name': '< 0,25 m/s',
                'marker': {'color': '#5e4fa2'},
                'type': 'barpolar',
            },
        ],
    )
