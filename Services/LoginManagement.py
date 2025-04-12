import traceback
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash
from DatabaseModels.Users import User
from DatabaseModels import DBConnections


class LoginManagement:
    def __init__(self):
        self.db = DBConnections

    def login_user(self, username: str, password: str) -> dict:
        try:
            with self.db.get_session() as session:

                # Get user by username only (not checking org_id)
                user = session.query(User).filter_by(user_name=username).first()

                if not user:
                    return {"status": False, "message": "User not found or invalid credentials"}

                if not user.is_active:
                    return {"status": False, "message": "User account is inactive"}

                # Check password (assuming stored as hashed)
                if not check_password_hash(user.password, password):
                    return {"status": False, "message": "Incorrect password"}

                # Update last login timestamp
                user.last_login = func.now()
                session.commit()

                return {
                    "status": True,
                    "message": "Login successful",
                    "user_id": user.user_id,
                    "user_name": user.user_name,
                    "email": user.email,
                    "org_id": user.org_id
                }

        except Exception as err:
            print(traceback.format_exc())
            return {"status": False, "message": str(err)}
