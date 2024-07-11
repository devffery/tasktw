from app import db
from models.user import User
from models.organisation import Organisation

db.create_all()
print("Database initialized!")
