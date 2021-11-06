from flask import Blueprint
from flask import render_template


views = Blueprint(name='views', import_name=__name__)


@views.route('/')
def index():
    with open('portal/static/locations.geojson') as f:
        geojson = f.read()

    return render_template(
        'index.html',
        title='Mülheim Daten Portal',
        geojson=geojson,
    )


@views.route('/compare')
def compare_data():
    return render_template(
        'compare.html',
        title='Stationsvergleich',
    )
