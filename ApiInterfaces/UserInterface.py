from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.UserManagement import UserManagement

organisation_bp = Blueprint('organisation_api', __name__)

org_service = UserManagement()


@organisation_bp.route('/createUser', methods=['POST'])
@jwt_required()
def create_user():
    user_data = request.json
    user_details = get_jwt_identity()
    print(user_details)
    result = org_service.create_user(user_data, "username")
    return jsonify(result)


@organisation_bp.route('/updateUser', methods=['PUT'])
@jwt_required()
def update_user():
    user_data = request.json
    user_details = get_jwt_identity()
    print(user_details)
    result = org_service.update_user(user_data, "username")
    return jsonify(result)


@organisation_bp.route('/getUsers', methods=['GET'])
@jwt_required()
def get_user():
    user_details = get_jwt_identity()
    org_id = user_details.get('org_id')
    print(user_details)
    result = org_service.get_users_by_org_id(org_id)
    return jsonify(result)


@organisation_bp.route('/deleteUsers', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_data = request.json
    user_details = get_jwt_identity()
    print(user_details)
    result = org_service.create_user(user_data, "username")
    return jsonify(result)
