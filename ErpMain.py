from flask import Flask, request, jsonify
from Services.UserManagement import UserManagement
from Services.OrganisationManagement import OrganisationManagement


app = Flask(__name__)
user_service = UserManagement()
org_service = OrganisationManagement()


@app.route('/createOrganisation', methods=['POST'])
def create_user():
    data = request.json

    org_data = data.get('org_data')
    user_data = data.get('user_data')

    username = request.headers.get("X-User", "system")
    result = org_service.create_org(org_data, user_data, username)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
