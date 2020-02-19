from flask import jsonify, request, make_response
import uuid, jwt, os
from datetime import datetime, timedelta

from . import main
from ..decorators import token_required
from ..models import User
from .. import db

@main.route("/user", methods = ['POST'])
def create_account():
    data = request.get_json()

    if all([data['username'], data['email'], data ['password']]):
        if User.query.filter_by(email = data['email'], username = data['username']).first():
            return jsonify({'status': 'ok', 'error': 'E401', 'message': 'Sorry, username or password already taken'})

        new_user = User(email = data['email'],  password = data['password'], public_id = str(uuid.uuid4()), username = data['username'])
        new_user.save()
        return jsonify({'status': 'ok','message': 'User Created Successfully' })
    else:
        return jsonify({'status': 'error', 'error': 'E402', 'message': 'Required Parameters Missing'})

@main.route("/user")
def login():
    auth = request.get_json()

    if not auth or not auth['email'] or not auth['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
        return jsonify({'status': 'error','status_code': 401, 'data': {'error': 'E4R3', 'message': 'User does not exist'}})
    else:
        if user.check_password(auth['password']):
            token_expiry = datetime.utcnow() + timedelta(minutes=60)
            token = jwt.encode({'public_id':user.public_id, 'exp': token_expiry}, str(os.environ.get('SECRET_KEY')))
        else:
            return jsonify({'status': 'error', 'error': '401', 'message': 'Authentication Failed'})

    return jsonify({'status': 'ok', 'data': {'token': token.decode('utf-8'), 'expiry': token_expiry.isoformat()}})

@main.route('/user', methods = ['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    if not data or not data.get('username'):
        return jsonify({'status': 'error', 'status_code': 401, 'data': {'message' : 'Required field username missing or empty'}})
    
    if data.get('username') is not None:
        if User.query.filter_by(username = data.get('username')).first():
            return jsonify({'status': 'error', 'data': {'message': 'Username already taken'}})
        else:
            current_user.username = data.get('username')
            db.session.commit()
            return jsonify({'status': 'ok', 'status_code': 200, 'data': {'message': 'Username changed successfully'}})

    