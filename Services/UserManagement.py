from sqlalchemy.exc import SQLAlchemyError
from DatabaseModels import DBConnections
from DatabaseModels.Users import User
import bcrypt


class UserManagement:
    def __init__(self):
        self.db = DBConnections

    def create_user(self, user_data: dict, username: str, session=None) -> dict:
        own_session = False  # Flag to track whether we created our own session

        try:
            if session is None:
                session = self.db.get_session()
                own_session = True  # We will handle commit/rollback
                session.__enter__()

            # Check if the email or username already exists for this organization
            existing_user = session.query(User).filter_by(
                email=user_data.get('email')
            ).first()
            print("existing_userexisting_user",existing_user)
            if existing_user:
                return {"status": False, "message": "Email already exists in this organisation"}

            existing_user_name = session.query(User).filter_by(
                user_name=user_data.get('user_name')
            ).first()
            print("existing_user_name",existing_user_name)
            if existing_user_name:
                return {"status": False, "message": "Username already exists in this organisation"}

            raw_password = user_data.get('password')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Create the new user
            new_user = User(
                user_name=user_data.get('user_name'),
                email=user_data.get('email'),
                password=hashed_password,  # Hash in real app!
                org_id=user_data.get('org_id'),
                age=user_data.get('age'),
                address=user_data.get('address'),
                is_active=user_data.get('is_active', True),
                created_by=username,
                created_by_program_name="UserManagement",
                updated_by=username,
                updated_by_program_name="UserManagement",
            )

            session.add(new_user)
            user_id = new_user.user_id
            if own_session:
                session.commit()

            return {
                "status": True,
                "message": "User created successfully",
                "user_id": user_id
            }

        except Exception as err:
            if own_session:
                session.rollback()
            return {"status": False, "message": str(err)}

        finally:
            if own_session:
                session.__exit__(None, None, None)

    def update_user(self, user_data: dict, username: str) -> dict:
        try:
            with self.db.get_session() as session:
                user_id = user_data.get("user_id")
                if not user_id:
                    return {"status": False, "message": "user_id is required in update_data"}

                user = session.query(User).filter_by(user_id=user_id).first()

                if not user:
                    return {"status": False, "message": "User not found"}

                # Check if the email or username already exists for this organization
                if "email" in user_data and user_data["email"] != user.email:
                    existing_user = session.query(User).filter_by(
                        org_id=user.org_id,
                        email=user_data["email"]
                    ).first()
                    if existing_user:
                        return {"status": False, "message": "Email already exists in this organisation"}

                if "user_name" in user_data and user_data["user_name"] != user.user_name:
                    existing_user_name = session.query(User).filter_by(
                        org_id=user.org_id,
                        user_name=user_data["user_name"]
                    ).first()
                    if existing_user_name:
                        return {"status": False, "message": "Username already exists in this organisation"}

                # Updating fields
                if "user_name" in user_data:
                    user.user_name = user_data["user_name"]

                if "email" in user_data:
                    user.email = user_data["email"]

                if "password" in user_data:
                    user.password = user_data["password"]  # Remember to hash the password

                if "age" in user_data:
                    user.age = user_data["age"]

                if "address" in user_data:
                    user.address = user_data["address"]

                if "is_active" in user_data:
                    user.is_active = user_data["is_active"]

                user.updated_by = username
                user.updated_by_program_name = "UserManagement"  # Example program name

                session.commit()

                return {"status": True, "message": "User updated successfully"}
        except SQLAlchemyError as err:
            return {"status": False, "message": str(err)}

    def get_users_by_org_id(self, org_id: int) -> dict:
        try:
            with self.db.get_session() as session:
                users = session.query(User).filter_by(org_id=org_id).all()

                if not users:
                    return {"status": False, "message": "No users found for the given organisation ID"}

                return {"status": True, "users": [user.user_name for user in users]}  # Adjust the data as needed
        except SQLAlchemyError as err:
            return {"status": False, "message": str(err)}

    def get_all_users(self) -> dict:
        try:
            with self.db.get_session() as session:
                users = session.query(User).all()

                if not users:
                    return {"status": False, "message": "No users found"}

                return {"status": True, "users": [user.user_name for user in users]}  # Adjust the data as needed
        except SQLAlchemyError as err:
            return {"status": False, "message": str(err)}
