from DatabaseModels import DBConnections
from DatabaseModels.UserRoles import UserRole
from sqlalchemy.exc import SQLAlchemyError


class UserRoleManagement:
    def __init__(self):
        self.db = DBConnections

    def create_user_role(self, user_id: int, role_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                # Check if the user-role relation already exists
                existing_user_role = session.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
                if existing_user_role:
                    return {"status": False, "message": "User already has this role"}

                # Create new user-role relation
                user_role = UserRole(user_id=user_id, role_id=role_id)

                session.add(user_role)
                session.commit()

                return {"status": True, "message": "User role created successfully"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def update_user_role(self, user_role_id: int, role_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                user_role = session.query(UserRole).filter_by(user_role_id=user_role_id).first()

                if not user_role:
                    return {"status": False, "message": "User-role relation not found"}

                # Update role
                user_role.role_id = role_id
                session.commit()

                return {"status": True, "message": "User role updated successfully"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def delete_user_role(self, user_role_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                user_role = session.query(UserRole).filter_by(user_role_id=user_role_id).first()

                if not user_role:
                    return {"status": False, "message": "User-role relation not found"}

                session.delete(user_role)
                session.commit()

                return {"status": True, "message": "User role deleted successfully"}
        except SQLAlchemyError as e:
            session.rollback()
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}

    def get_user_roles(self, org_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                user_roles = session.query(UserRole).filter_by(user_id=org_id).all()

                if not user_roles:
                    return {"status": False, "message": "No roles found for this user"}

                result = [
                    {"user_role_id": ur.user_role_id, "role_id": ur.role_id}
                    for ur in user_roles
                ]

                return {"status": True, "data": result}
        except SQLAlchemyError as e:
            return {"status": False, "message": f"Error: {str(e)}"}
        except Exception as e:
            return {"status": False, "message": str(e)}
