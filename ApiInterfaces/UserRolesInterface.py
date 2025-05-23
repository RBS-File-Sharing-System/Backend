from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Services.UserRoleManagement import UserRoleManagement

organisation_bp = Blueprint('roles_api', __name__)

roles_service = UserRoleManagement()


@organisation_bp.route('/createRoles', methods=['POST'])
@jwt_required()
def create_role():
    role_data = request.json
    user_details = get_jwt_identity()
    print(user_details)
    result = roles_service.create_user_role(role_data, "username")
    return jsonify(result)


@organisation_bp.route('/updateRoles', methods=['PUT'])
@jwt_required()
def update_role():
    role_data = request.json
    user_details = get_jwt_identity()
    print(user_details)
    result = roles_service.update_user_role(role_data, "username")
    return jsonify(result)


@organisation_bp.route('/getUserRoles', methods=['GET'])
@jwt_required()
def get_role():
    user_details = get_jwt_identity()
    org_id = user_details.get('org_id')
    print(user_details)
    result = roles_service.get_user_roles(org_id)
    return jsonify(result)


@organisation_bp.route('/deleteUserRoles', methods=['DELETE'])
@jwt_required()
def delete_role():
    user_role_id = request.args.get('user_role_id')
    try:
        user_role_id = int(user_role_id)
    except:
        return {"status": False, "message":"Incorrect Role Id"}
    result = roles_service.delete_user_role(user_role_id)
    return jsonify(result)
