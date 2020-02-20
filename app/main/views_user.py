from flask import jsonify, request, make_response
import uuid, jwt, os
from datetime import datetime, timedelta

from . import main
from ..decorators import token_required
from ..models import User, ApiResponse
from .. import db

@main.route("/user/register", methods = ['POST'])
def create_account():
    data = request.get_json()

    if data is not None:
        if all([data.get('username'), data.get('email'), data.get('password')]):
            if User.query.filter_by(email = data['email'], username = data['username']).first():
                response = ApiResponse('ok', {'message': 'Sorry, username or email already taken'})
                return jsonify(response.__dict__)                                                                                                                                                                         

            new_user = User(email = data['email'],  password = data['password'], public_id = str(uuid.uuid4()), username = data['username'])
            new_user.save()

            response = ApiResponse('ok', {'message': 'User Created Successfully', 'public_id': new_user.public_id})
            return jsonify(response.__dict__)
        else:
            response = ApiResponse('error', {'message': 'Required Parameters Missing'})
            return jsonify(response.__dict__), 401
    else:
        response = ApiResponse('error', {'message': 'Required Parameters Cannot be empty'})
        return jsonify(response.__dict__), 401

@main.route("/user/login", methods = ['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth['email'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
        response = ApiResponse('ok', {'message': 'User does not exist'})
        return jsonify(response.__dict__), 401
    else:
        if user.check_password(auth['password']):
            token_expiry = datetime.utcnow() + timedelta(minutes=60)
            token = jwt.encode({'public_id':user.public_id, 'exp': token_expiry}, str(os.environ.get('SECRET_KEY')))
        else:
            response = ApiResponse('ok', {'message': 'Authentication Failed'})
            return jsonify(response.__dict__), 401

    response = ApiResponse('ok', {'token': token.decode('utf-8'), 'expiry': token_expiry.isoformat(), 'public_id': user.public_id})
    return jsonify(response.__dict__)

@main.route('/user/update', methods = ['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    if not data or not data.get('username'):
        response = ApiResponse('error', {'message' : 'Required field username missing or empty'})
        return jsonify(response.__dict__), 401
    
    if data.get('username') is not None:
        if User.query.filter_by(username = data.get('username')).first():
            response = ApiResponse('error', {'message': 'Username already taken'})
            return jsonify(response.__dict__), 422
        else:
            current_user.username = data.get('username')
            db.session.commit()
            response = ApiResponse('ok', {'message': 'Username changed successfully', 'public_id': current_user.public_id})
            return jsonify(response.__dict__), 200
        