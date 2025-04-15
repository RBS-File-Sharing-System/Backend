from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from ApiInterfaces.OrganisationInterface import organisation_bp
from ApiInterfaces.UserInterface import user_bp
from ApiInterfaces.LoginInterface import login_bp
from flask_cors import CORS

# Flask app and configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to a real secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to a real secret key
CORS(app)


# Initialize JWT
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(organisation_bp, url_prefix='/api/organisation')
app.register_blueprint(login_bp, url_prefix='/api/login')
app.register_blueprint(user_bp, url_prefix='/api/users')



@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()  # Get current user's identity from JWT token
    return jsonify({"message": f"Hello, {current_user}!"})


if __name__ == '__main__':
    app.run(debug=True)
