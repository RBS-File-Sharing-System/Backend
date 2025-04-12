from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, func
from DatabaseModels.DBConnections import Base

PROGRAM_NAME = "default"


class UserRole(Base):
    __tablename__ = 'user_roles'
    __table_args__ = {'schema': 'config'}

    user_role_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('config.users.user_id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('config.roles.role_id', ondelete='CASCADE'), nullable=False)

    # Audit fields (with proper default and onupdate)
    creation_date = Column(DateTime, default=func.now())
    created_by = Column(String, nullable=True)
    created_by_program_name = Column(String, default=PROGRAM_NAME)

    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    updated_by_program_name = Column(String, default=PROGRAM_NAME, onupdate=PROGRAM_NAME)
