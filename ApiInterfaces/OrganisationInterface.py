from flask import Blueprint, request, jsonify
from Services.OrganisationManagement import OrganisationManagement

organisation_bp = Blueprint('organisation_api', __name__)

org_service = OrganisationManagement()


@organisation_bp.route('/createOrganisation', methods=['POST'])
def create_organisation():
    data = request.json
    org_data = data.get('org_data')
    user_data = data.get('user_data')
    username = user_data.get('user_name')
    result = org_service.create_org(org_data, user_data, username)
    print(result)
    return jsonify(result)
