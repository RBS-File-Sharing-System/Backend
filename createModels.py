# DatabaseModels/drop_and_create_tables.py

from DatabaseModels.DBConnections import Base, engine
from DatabaseModels.Organisations import Organisation
from DatabaseModels.Users import User

# Drop all tables (if they exist)
Base.metadata.drop_all(engine)

# Create all tables
Base.metadata.create_all(engine)

print("Tables have been dropped and recreated successfully.")
