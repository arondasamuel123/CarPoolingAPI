from flask import jsonify

from . import main
from ..models import ApiResponse

@main.app_errorhandler(404)
def error404(error):
    response = ApiResponse('error', {'message': 'Endpoint was not found. Known endpoints include /user, /workspace'})
    return jsonify(response.__dict__),404

@main.app_errorhandler(500)
def error500(error):
    response = ApiResponse('error', {'message': 'An Error occurred'})
    return jsonify({response.__dict__}), 500