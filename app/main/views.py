from flask import jsonify, request, make_response
import uuid, jwt, os
from datetime import datetime, timedelta

from . import main
from ..decorators import token_required
from ..models import User, Workspace, ApiResponse, Car
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
        
@main.route('/workspaces', methods=['GET'])
@token_required
def get_workspaces():
    data = request.get_json()
    
    workspaces = Workspace.query.all()
    
    output = []
    for workspace in workspaces:
        workspace_data= {}
        workspace_data['name']= workspace.name
        workspace_data['admin_id']= workspace.admin_id
        workspace_data['description']= workspace.description
        output.append(workspace_data)

    response = ApiResponse('ok', {'workspaces': output})
    return jsonify(response.__dict__)

@main.route('/workspace/<public_id>', methods=['GET'])
@token_required
def get_workspace_by_id(current_user, public_id):
    data = request.get_json()
    
    workspace = Workspace.query.filter_by(admin_id=current_user.public_id).all()
    output = []

    for work in workspace:
        work_data = {}
        work_data['name']= work.name
        work_data['description'] = work.description
        output.append(work_data)
    
    response = ApiResponse('ok', {'workspace': output})
    return jsonify(response.__dict__)

@main.route('/workspace', methods=['POST'])
@token_required
def create_workspace(current_user):
    data = request.get_json()
    workspace = Workspace.query.filter_by(admin_id=current_user.public_id, name = data['name']).first()
    
    new_workspace = Workspace(name=data['name'], description=data['description'], admin_id=current_user.public_id)
    
    if  workspace:
        response = ApiResponse('ok', {'message': 'Workspace exists'})
        return jsonify(response.__dict__)
    else:
        new_workspace.save()
        response = ApiResponse('ok', {'message': 'Workspace created successfully'})
        return jsonify(response.__dict__)
    
@main.route('/workspace/<admin_id>', methods=['DELETE'])
@token_required
def delete_workspace(current_user, admin_id):
    data =request.get_json()
    delete_workspace = Workspace.query.filter_by(admin_id=current_user.public_id).first()
    delete_workspace.delete_space()
    
    response = ApiResponse('ok', {'message':"Workspace deleted"})
    return jsonify(response.__dict__)

@main.route('cars', methods = ['POST'])
@token_required
def create_car(current_user):
    data = requets.get_json()

    car = Car.query.filter_by(workspace_id=workspace_id).first()

    new_car = Workspace(owner_name=data['owner_name'], noofseats=data['noofseats'], workspace_id=workspace_id, license_plate=data['license_plate'])


@main.route('/cars/<int:id>', methods =['DELETE'])
@token_required
def delete_car(current_user,id):
    delete_car = Car.query.filter_by(id=id).first()
    delete_car.delete_car()

@main.route('/cars/<int:id>', methods =['GET'])
@token_required
def get_car_by_workspace_id(current_user,workspace_id):
    my_car = Car.query.filter_by(workspace_id=workspace_id).first()

    




        

    
    

    