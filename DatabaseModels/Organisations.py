import sys
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from DatabaseModels.DBConnections import Base, engine

# Get the name of the program being run
PROGRAM_NAME = sys.argv[0] if sys.argv else "unknown"


class Organisation(Base):
    __tablename__ = "organisations"
    __table_args__ = {'schema': 'config'}

    org_id = Column(Integer, primary_key=True, autoincrement=True)
    org_name = Column(String, nullable=False)
    org_email = Column(String, unique=True, nullable=False)

    # Audit fields
    creation_date = Column(DateTime, default=func.now())
    created_by = Column(String, nullable=True)
    created_by_program_name = Column(String, default=PROGRAM_NAME)

    # Relationship with User (optional, if you want to access users via organisation)
    users = relationship("User", backref="organisation", lazy="dynamic")

    update_date = Column(DateTime, default=func.now(), onupdate=func.now())
    updated_by = Column(String, nullable=True)
    updated_by_program_name = Column(String, default=PROGRAM_NAME, onupdate=PROGRAM_NAME)


# Create the table in the database
Base.metadata.create_all(engine)
