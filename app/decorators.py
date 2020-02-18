from functools import wraps

import jwt, os
from flask import request, jsonify

from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[-1]
        else:
            return jsonify({'message': 'Token is missing'})

        try: 
            data = jwt.decode(token, os.environ.get('SECRET_KEY'))
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'status': 'error', 'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
