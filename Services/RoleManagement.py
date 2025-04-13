from sqlalchemy.exc import SQLAlchemyError
from DatabaseModels import DBConnections
from DatabaseModels.Roles import Role


class RoleManagement:
    def __init__(self):
        self.db = DBConnections

    def create_role(self, role_data: dict, username: str) -> dict:
        try:
            with self.db.get_session() as session:
                # Check if role already exists
                existing_role = session.query(Role).filter_by(role_name=role_data['role_name']).first()
                if existing_role:
                    return {"status": False, "message": "Role already exists"}

                # Create new role
                new_role = Role(
                    role_name=role_data['role_name'],
                    description=role_data.get('description'),
                    created_by=username,
                    updated_by=username
                )

                session.add(new_role)
                session.commit()

                return {"status": True, "message": "Role created successfully", "role_id": new_role.role_id}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def update_role(self, role_data: dict, username: str) -> dict:
        role_id = role_data.get('role_id')
        try:
            with self.db.get_session() as session:
                role = session.query(Role).filter_by(role_id=role_id).first()

                if not role:
                    return {"status": False, "message": "Role not found"}

                # Update role details
                role.role_name = role_data.get('role_name', role.role_name)
                role.description = role_data.get('description', role.description)
                role.updated_by = username

                session.commit()

                return {"status": True, "message": "Role updated successfully"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def delete_role(self, role_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                role = session.query(Role).filter_by(role_id=role_id).first()

                if not role:
                    return {"status": False, "message": "Role not found"}

                session.delete(role)
                session.commit()

                return {"status": True, "message": "Role deleted successfully"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def get_all_roles(self) -> dict:
        try:
            with self.db.get_session() as session:
                roles = session.query(Role).all()

                if not roles:
                    return {"status": False, "message": "No roles found"}

                result = [
                    {"role_id": role.role_id, "role_name": role.role_name, "description": role.description}
                    for role in roles
                ]

                return {"status": True, "data": result}
        except SQLAlchemyError as e:
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def get_roles_by_org_id(self, org_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                roles = session.query(Role).filter_by(org_id=org_id).all()

                if not roles:
                    return {"status": False, "message": "No roles found for this organization"}

                result = [
                    {"role_id": r.role_id, "role_name": r.role_name, "description": r.description}
                    for r in roles
                ]

                return {"status": True, "data": result}
        except SQLAlchemyError as e:
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}
