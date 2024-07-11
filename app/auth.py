from flask import Blueprint, request, jsonify
from .models import User, Organisation, db
from . import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ["firstName", "lastName", "email", "password"]
    errors = {"errors": []}

    for field in required_fields:
        if field not in data or not data[field]:
            errors["errors"].append({"field": field, "message": f"{field} is required"})

    if "email" in data and User.query.filter_by(email=data["email"]).first():
        errors["errors"].append({"field": "email", "message": "Email already exists"})

    if errors["errors"]:
        return jsonify(errors), 422

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    user = User(
        firstName=data["firstName"],
        lastName=data["lastName"],
        email=data["email"],
        password=hashed_password,
        phone=data.get("phone")
    )

    db.session.add(user)
    db.session.commit()

    org_name = f"{user.firstName}'s Organisation"
    organisation = Organisation(name=org_name, creator=user)
    db.session.add(organisation)
    db.session.commit()

    access_token = create_access_token(identity=str(user.userId))

    return jsonify({
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": user.to_dict(),
            "organisation": {
                "orgId": str(organisation.orgId),
                "name": organisation.name
            }
        }
    }), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ["email", "password"]
    errors = {"errors": []}

    for field in required_fields:
        if field not in data or not data[field]:
            errors["errors"].append({"field": field, "message": f"{field} is required"})

    if errors["errors"]:
        return jsonify(errors), 422

    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=str(user.userId))
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": access_token,
                "user": user.to_dict(),
                "organisations": [{"orgId": str(org.orgId), "name": org.name} for org in user.organisations]
            }
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid credentials",
        "statusCode": 401
    }), 401

@auth.route('/token/verify', methods=['GET'])
@jwt_required()
def verify_token():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({
            "status": "success",
            "message": "Token is valid",
            "data": {
                "user": user.to_dict()
            }
        }), 200
    return jsonify({
        "status": "error",
        "message": "Token is invalid",
        "statusCode": 401
    }), 401
