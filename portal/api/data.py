from flask import Blueprint
from flask import jsonify
from flask import Response


api = Blueprint(name='api', import_name=__name__,  url_prefix='/api')


@api.route('/')
def test() -> Response:
    return jsonify({'hello': 'world'})
