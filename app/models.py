from . import db
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    userId = Column(String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    phone = Column(String(15), nullable=True)
    organisations = db.relationship('Organisation', backref='creator', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "userId": self.userId,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "phone": self.phone,
        }

    def __repr__(self):
        return f"<User {self.email}>"

organisation_members = db.Table('organisation_members',
    Column('user_id', String(36), ForeignKey('users.userId'), primary_key=True),
    Column('organisation_id', String(36), ForeignKey('organisations.orgId'), primary_key=True)
)

class Organisation(db.Model):
    __tablename__ = 'organisations'
    orgId = Column(String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    creator_id = Column(String(36), ForeignKey('users.userId'), nullable=False)
    members = db.relationship('User', secondary='organisation_members', backref='member_organisations')

    def to_dict(self):
        return {
            "orgId": self.orgId,
            "name": self.name,
            "description": self.description,
        }

    def __repr__(self):
        return f"<Organisation {self.name}>"
