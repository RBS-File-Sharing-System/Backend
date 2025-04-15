from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from DatabaseModels.DBConnections import Base, engine


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'config'}

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey('config.organisations.org_id'), nullable=False)
    email = Column(String, unique=True, nullable=False)

    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Store hashed password, not plain text

    # Personal Details
    age = Column(Integer, nullable=True)
    address = Column(String, nullable=True)

    # Active status
    is_active = Column(Boolean, default=True)  # Indicating whether the user is active or not
    is_admin = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)  # The last time the user logged in

    # Relationship with Organisation
    organisation = relationship("Organisation", backref="org_users")

    # Default columns
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

    # Program name columns
    created_by_program_name = Column(String, nullable=False)
    updated_by_program_name = Column(String, nullable=False)

