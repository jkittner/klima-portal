from flask import Blueprint
from flask import jsonify
from flask import request
from flask import Response

from portal.api.utils import connect

api = Blueprint(name='api', import_name=__name__,  url_prefix='/api')


@api.route('/data')
def test() -> Response:
    print(request.args['station'])
    with connect('app.db') as db:
        ret = db.execute(
            '''\
            SELECT datum as "[timestamp]", lufttemp_200
            FROM measurements WHERE station = ?
            ''',
            (request.args['station'],),
        ).fetchall()
    return jsonify(
        {
            'x': [i[0].isoformat() for i in ret],
            'y': [i[1] for i in ret],
            'type': 'scatter',
        },
    )
