from flakon import JsonBlueprint
from flask import jsonify, request, Blueprint, url_for, g, request_finished

# home = JsonBlueprint('home', __name__)
from werkzeug.exceptions import Unauthorized, NotAcceptable
from werkzeug.routing import BaseConverter, ValidationError

# def add_app_url_map_converter(self, func, name=None):
#     def register_converter(state):
#         state.app.url_map.converters[name or func.__name__] = func
#
#     self.record_once(register_converter)
#
# # monkey-patch the Blueprint object to allow addition of URL map converters
# Blueprint.add_app_url_map_converter = add_app_url_map_converter

home = Blueprint('home', __name__)


@home.before_request
def authenticate():
    if request.authorization:
        if (request.authorization['username'], request.authorization['password']) == ('admin', 'admin'):
            g.user = request.authorization['username']
        else:
            raise Unauthorized()
    else:
        g.user = 'Anonymous'

def finished(sender, response, **extra):
    print('Finishing request')

request_finished.connect(finished)

# @home.route('/' methods=['POST', 'DELETE', 'GET'])
@home.route('/')
def index():
    user = g.user
    return f"{{'message': 'Home View', 'user': {user} }}", 202, {'Content-Type': 'application/json'}

@home.route('/converter/<int:my_int>')
def converter(my_int):
    return jsonify({
        'message': 'Converter',
        'my_int': my_int
    })

class DummyConverter(BaseConverter):
    def to_python(self, value):
        if value.isdigit() and int(value) % 2 == 0:
            return value
        else:
            # raise ValidationError()
            raise NotAcceptable()
    def to_url(self, value):
        return 'empty_number' # just to use this option...




# home.add_app_url_map_converter(DummyConverter, 'is_even')

@home.route('/custom_converter')
@home.route('/custom_converter/<is_even:my_int>')
def custom_converter(my_int=None):
    return jsonify({
        'message': 'Converter',
        'my_int': my_int if my_int else url_for('home.custom_converter', my_int='whatever')
    })


