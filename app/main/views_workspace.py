from flask import jsonify, request, make_response
import uuid, jwt, os
from datetime import datetime, timedelta
from string import digits
from random import SystemRandom

from . import main
from ..decorators import token_required
from ..models import User, Workspace, ApiResponse, WorkspaceInvite, WorkspaceUser
from .. import db
from ..email import mail_message

@main.route('/workspaces', methods=['GET'])
@token_required
def get_workspaces(current_user):
    data = request.get_json()
    
    workspaces = Workspace.query.all()
    
    output = []
    for workspace in workspaces:
        workspace_data= {}
        workspace_data['name']= workspace.name
        workspace_data['admin_id']= workspace.admin_id
        workspace_data['workspace_id']=workspace.public_id
        workspace_data['description']= workspace.description
        output.append(workspace_data)

    response = ApiResponse('ok', {'workspaces': output})
    return jsonify(response.__dict__)

@main.route('/workspace/created', methods=['GET'])
@token_required
def get_workspace_by_id(current_user):
    data = request.get_json()
    
    workspace = Workspace.query.filter_by(admin_id=current_user.public_id).all()
    output = []

    for work in workspace:
        work_data = {}
        work_data['name']= work.name
        work_data['description'] = work.description
        work_data['workspace_id'] = work.public_id
        output.append(work_data)
    
    response = ApiResponse('ok', {'workspaces': output})
    return jsonify(response.__dict__)

@main.route('/workspace/invite', methods = ['POST'])
@token_required
def workspace_invite(current_user):
    data = request.get_json()
    if not data or not data.get('workspace_id') or not data.get('email'):
        response = ApiResponse('error', {'message': 'required field workspace_id or email missing'})
    else:
        my_workspace = Workspace.query.filter_by(admin_id= current_user.public_id, public_id = data.get('workspace_id')).first()
        if my_workspace:
            join_code = ''.join(SystemRandom().choices(digits, k=8))
            new_invite = WorkspaceInvite(workspace_id = my_workspace.public_id, email = data.get('email'), join_code = join_code, confirmed = False)
            new_invite.save()
            mail_message('Invitation to workspace', 'email/invite_user', new_invite.email, workspace = my_workspace, invite = new_invite)
            response = ApiResponse('ok', {'message': 'An invite has been sent'})
            return jsonify(response.__dict__)
        else:
            response = ApiResponse('error', {'message': 'No workspace found'})
            return jsonify(response.__dict__)

@main.route('/workspace/create', methods=['POST'])
@token_required
def create_workspace(current_user):
    data = request.get_json()
    workspace = Workspace.query.filter_by(admin_id=current_user.public_id, name = data['name']).first()
    
    new_workspace = Workspace(name=data['name'], description=data['description'], admin_id=current_user.public_id, public_id = uuid.uuid4())
    
    if  workspace:
        response = ApiResponse('ok', {'message': 'Workspace exists'})
        return jsonify(response.__dict__)
    else:
        new_workspace.save()
        response = ApiResponse('ok', {'message': 'Workspace created successfully', 'workspace_id': new_workspace.public_id})
        return jsonify(response.__dict__)

@main.route('/workspace/verify', methods = ['POST'])
@token_required
def join_workspace(current_user):
    data = request.get_json()

    if not data or not data.get('join_code') or not data.get('workspace_id'):
        response = ApiResponse('ok', {'message':"Required field join_code or workspace_id missing"})
        return jsonify(response.__dict__)

    else:
        invite = WorkspaceInvite.query.filter_by(email = current_user.email, workspace_id = data.get('workspace_id'), join_code = data.get('join_code')).all()[-1]

        if not invite:
            response = ApiResponse('ok', {'message': 'Something was not right'})
            return jsonify(response.__dict__)
        else:
            new_workspace_user = WorkspaceUser(workspace_id = data.get('workspace_id'), user = current_user)
            invite.confirmed = True
            db.session.commit()
            new_workspace_user.save()

            response = ApiResponse('ok', {'message': f'You have been confirmed to workspace id <{new_workspace_user.workspace_id}>'})
            return jsonify(response.__dict__)

@main.route('/workspace/<admin_id>', methods=['DELETE'])
@token_required
def delete_workspace(current_user, admin_id):
    data =request.get_json()
    delete_workspace = Workspace.query.filter_by(admin_id=current_user.public_id).first()
    delete_workspace.delete_space()
    
    response = ApiResponse('ok', {'message':"Workspace deleted"})
    return jsonify(response.__dict__)