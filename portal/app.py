from flask import Flask

from portal.api.data import api
from portal.config import Config
from portal.dashboard.views import views

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api)
app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=True)
