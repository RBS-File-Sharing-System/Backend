from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from Services.UserManagement import UserManagement

user_bp = Blueprint('user_api', __name__)

user_service = UserManagement()


@user_bp.route('/createUser', methods=['POST'])
@jwt_required()
def create_user():
    user_data = request.json
    user_details = get_jwt()
    org_id = user_details['org_id']
    user_data['org_id'] = org_id
    print("user_data:::1",user_data)
    result = user_service.create_user(user_data, "username")
    return jsonify(result)


@user_bp.route('/updateUser', methods=['PUT'])
@jwt_required()
def update_user():
    user_data = request.json
    user_details = get_jwt()
    result = user_service.update_user(user_data, "username")
    return jsonify(result)


@user_bp.route('/getUsers', methods=['GET'])
@jwt_required()
def get_user():
    user_details = get_jwt()
    print("user_details",user_details)
    org_id = user_details.get('org_id')
    result = user_service.get_users_by_org_id(org_id)
    return jsonify(result)


@user_bp.route('/deleteUsers', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_data = request.json
    user_details = get_jwt()
    result = user_service.create_user(user_data, "username")
    return jsonify(result)
