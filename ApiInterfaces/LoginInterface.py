from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from Services.LoginManagement import LoginManagement

login_bp = Blueprint('login_api', __name__)

login_service = LoginManagement()


@login_bp.route('/login', methods=['POST'])
def login():
    username = request.authorization.get('username')
    password = request.authorization.get('password')

    if not username or not password:
        return jsonify({"status": False, "message": "Username and Password are required"}), 400

    # Fetch user from DB
    result = login_service.login_user(username, password)
    if not result['status']:
        return jsonify(result), 401  # Return error if login fails

    # Generate JWT token upon successful login
    access_token = create_access_token(identity=username)

    return jsonify({
        "status": True,
        "message": "Login successful",
        "access_token": access_token
    })
