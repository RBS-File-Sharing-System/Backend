from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from Services.UserManagement import UserManagement
from Services.OrganisationManagement import OrganisationManagement
from Services.LoginManagement import LoginManagement

app = Flask(__name__)

# Flask JWT Extended Setup
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to a real secret key
jwt = JWTManager(app)

user_service = UserManagement()
org_service = OrganisationManagement()
login_service = LoginManagement()


@app.route('/createOrganisation', methods=['POST'])
def create_organisation():
    data = request.json

    org_data = data.get('org_data')
    user_data = data.get('user_data')

    username = request.headers.get("X-User", "system")
    result = org_service.create_org(org_data, user_data, username)
    return jsonify(result)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

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


# Example of a protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Get current user's identity from JWT token
    return jsonify({"message": f"Hello, {current_user}!"})


if __name__ == '__main__':
    app.run(debug=True)
