from flask import Blueprint
from flask import render_template
from flask import Response
from flask import send_from_directory


views = Blueprint(name='views', import_name=__name__)


@views.route('/')
def index() -> str:
    with open('portal/static/locations.geojson') as f:
        geojson = f.read()

    return render_template(
        'index.html',
        title='Mülheim Daten Portal',
        geojson=geojson,
    )


@views.route('/compare')
def compare_data() -> str:
    return render_template(
        'compare.html',
        title='Stationsvergleich',
    )


@views.route('/results')
def results() -> str:
    return render_template(
        'results.html',
        title='Untersuchungsergebnisse',
    )


@views.route('/favicon.ico')
def favicon() -> Response:
    return send_from_directory(
        directory='static/img',
        path='logo.svg',
    )


@views.route('/robots.txt')
def robots() -> Response:
    return send_from_directory(
        directory='static',
        path='robots.txt',
    )
