from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from DatabaseModels.DBConnections import Base

PROGRAM_NAME = "default"


class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'config'}

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # Audit fields
    creation_date = Column(DateTime, default=func.now())
    created_by = Column(String, nullable=True)
    created_by_program_name = Column(String, default=PROGRAM_NAME)
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    updated_by_program_name = Column(String, default=PROGRAM_NAME, onupdate=PROGRAM_NAME)

    # Relationship
    users = relationship('User', secondary='config.user_roles', back_populates='roles')
