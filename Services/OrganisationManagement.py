import traceback
from DatabaseModels import DBConnections
from DatabaseModels.Organisations import Organisation
from UserManagement import UserManagement


class OrganisationManagement:
    def __init__(self):
        self.db = DBConnections
        self.user_service = UserManagement()

    def create_org(self, org_data: dict, user_data: dict, username: str) -> dict:
        try:
            with self.db.get_session() as session:
                existing_org = session.query(Organisation).filter(
                    (Organisation.org_name == org_data.get('org_name')) |
                    (Organisation.org_email == org_data.get('org_email'))
                ).first()

                # validating unique values for org_name and org_email
                if existing_org:
                    if existing_org.org_name == org_data.get('org_name'):
                        return {"status": False, "message": "Organisation name already exists"}
                    if existing_org.org_email == org_data.get('org_email'):
                        return {"status": False, "message": "Organisation email already exists"}

                # Creating Organisation
                org = Organisation(
                    org_name=org_data.get('org_name'),
                    org_email=org_data.get('org_email'),
                    created_by=username,
                    created_by_program_name=str(__class__),
                    updated_by=username,
                    updated_by_program_name=str(__class__)
                )

                session.add(org)
                session.flush()

                org_id = org.org_id
                user_data['org_id'] = org_id

                # Creating User
                create_user_response = self.user_service.create_user(user_data, username)
                if not create_user_response.get('status'):
                    return create_user_response

                session.commit()
                return {
                    "status": True,
                    "message": "Organisation created successfully",
                    "org_id": org.org_id
                }

        except Exception as er:
            print(traceback.format_exc())
            return {"status": False, "message": str(er)}

    def update_org(self, update_data: dict, username: str) -> dict:
        try:
            org_id = update_data.get("org_id")
            if not org_id:
                return {"status": False, "message": "org_id is required in update_data"}

            with self.db.get_session() as session:
                org = session.query(Organisation).filter_by(org_id=org_id).first()

                if not org:
                    return {"status": False, "message": "Organisation not found"}

                # Check for org_name conflict
                if "orgName" in update_data:
                    name_conflict = session.query(Organisation).filter(
                        Organisation.org_name == update_data["org_name"],
                        Organisation.org_id != org_id
                    ).first()
                    if name_conflict:
                        return {"status": False, "message": "Organisation name already exists"}

                # Check for org_email conflict
                if "orgEmail" in update_data:
                    email_conflict = session.query(Organisation).filter(
                        Organisation.org_email == update_data["org_email"],
                        Organisation.org_id != org_id
                    ).first()
                    if email_conflict:
                        return {"status": False, "message": "Organisation email already exists"}

                # Apply updates
                if 'org_name' in update_data:
                    org.org_name = update_data.get('org_name')
                if 'org_email' in update_data:
                    org.org_email = update_data.get('org_email')

                org.updated_by = username
                org.updated_by_program_name = str(__class__)

                session.commit()

                return {"status": True, "message": "Organisation updated successfully"}

        except Exception as er:
            print(traceback.format_exc())
            return {"status": False, "message": str(er)}


if __name__ == "__main__":
    obj = OrganisationManagement()
    data = {"org_name": "testOrg5", "org_email": "krishna2@gmail.com", 'org_id': 4}
    print(obj.update_org(data, 'update_user'))
