from flask import jsonify, request, make_response
import uuid, jwt, os
from datetime import datetime, timedelta

from . import main
from ..decorators import token_required
from ..models import User, Workspace, ApiResponse, Car, WorkspaceInvite
from .. import db

@main.route('/cars/create', methods = ['POST'])
@token_required
def create_car(current_user):
    data = request.get_json()
    print(current_user)

    if not data or not data.get('seats') or not data.get('workspace_id') or not data.get('license_plate'):
        response = ApiResponse('error', {'message' : 'Required fields seats, workspace_id or license_plate missing'})
        return jsonify(response.__dict__), 401

    car = Car.query.filter_by(license_plate = data.get('license_plate')).first()

    if car:
        response = ApiResponse('error', {'message': 'Car already exists'})
        return jsonify(response.__dict__)
    else:
        new_car = Car(owner_name=current_user.username, noofseats=data['seats'], workspace = Workspace.query.filter_by(public_id = data.get('workspace_id')).first(), license_plate=data['license_plate'], public_id = uuid.uuid4())
        new_car.save()
        response = ApiResponse('ok', {'message': 'New car added succesfully', 'public_id': new_car.public_id})
        return jsonify(response.__dict__)

@main.route('/cars/<int:car_id>', methods =['DELETE'])
@token_required
def delete_car(current_user,id):
    delete_car = Car.query.filter_by(id=id).first()
    delete_car.delete_car()

@main.route('/cars/<int:id>', methods =['GET'])
@token_required
def get_car_by_workspace_id(current_user,workspace_id):
    my_car = Car.query.filter_by(workspace_id=workspace_id).first()

@main.route('/cars', methods = ['GET'])
@token_required
def list_workspace_cars(current_user):
    arg = request.args.get('workspace_id')

    if arg is not None:
        user_workspace = Workspace.query.filter_by(public_id = arg).first()
        if user_workspace:
            workspace_cars = Car.query.filter_by(workspace = user_workspace).all()
            output = []

            for wcar in workspace_cars:
                car_data = {}
                car_data['owner_name'] = wcar.owner_name
                car_data['total_seats'] = wcar.noofseats
                car_data['license_plate'] = wcar.license_plate
                car_data['public_id'] = wcar.public_id
                output.append(car_data)

            response = ApiResponse('ok', {'cars': output, 'workspace_id': user_workspace.public_id, 'workspace_name': user_workspace.name})
            return jsonify(response.__dict__)
        else:
            response = ApiResponse('error', {'message': 'Incorrect workspace_id provided'})
            return jsonify(response.__dict__)

    else:
        response = ApiResponse('error', {'message': 'Required parameter workspace_id is missing'})
        return jsonify(response.__dict__)