import os
from flakon import create_app
from flask import Flask
from konfig import Config

from myservice.views import blueprints
from myservice.views.home import DummyConverter

_HERE = os.path.dirname(__file__)
settings = os.path.join(_HERE, 'settings.ini')

# app = create_app(blueprints=blueprints, settings=_SETTINGS)


app = Flask(__name__)

# load configuration
settings = os.environ.get('FLASK_SETTINGS', settings)
if settings is not None:
    app.config_file = Config(settings)
    app.config.update(app.config_file.get_map('flask'))

app.url_map.converters.update({'is_even': DummyConverter})

# register blueprints
if blueprints is not None:
    for bp in blueprints:
        app.register_blueprint(bp)





