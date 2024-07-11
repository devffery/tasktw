from flask import Blueprint, request, jsonify
from .models import User, Organisation, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid

views = Blueprint('views', __name__)

def generate_error_response(message, status_code):
    return jsonify({"status": "error", "message": message, "statusCode": status_code}), status_code

@views.route('/users/<id>', methods=['GET'])
@jwt_required()
def get_user(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(id)

    if not user:
        return generate_error_response("User not found", 404)

    current_user = User.query.get(current_user_id)

    if str(current_user.userId) != id and not any(org in current_user.organisations for org in user.organisations):
        return generate_error_response("Access forbidden", 403)

    return jsonify({
        "status": "success",
        "message": "User retrieved successfully",
        "data": user.to_dict()
    }), 200

@views.route('/organisations', methods=['GET'])
@jwt_required()
def get_organisations():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return generate_error_response("User not found", 404)

    organisations = user.organisations
    return jsonify({
        "status": "success",
        "message": "Organisations retrieved successfully",
        "data": [org.to_dict() for org in organisations]
    }), 200

@views.route('/organisations/<orgId>', methods=['GET'])
@jwt_required()
def get_organisation(orgId):
    current_user_id = get_jwt_identity()
    org = Organisation.query.get(orgId)
    user = User.query.get(current_user_id)

    if not org:
        return generate_error_response("Organisation not found", 404)

    if org not in user.organisations:
        return generate_error_response("Access forbidden", 403)

    return jsonify({
        "status": "success",
        "message": "Organisation retrieved successfully",
        "data": org.to_dict()
    }), 200

@views.route('/organisations', methods=['POST'])
@jwt_required()
def create_organisation():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return generate_error_response("Name is required", 422)

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return generate_error_response("User not found", 404)

    organisation = Organisation(name=name, description=description, creator=user)
    db.session.add(organisation)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Organisation created successfully",
        "data": organisation.to_dict()
    }), 201

@views.route('/organisations/<orgId>/users', methods=['POST'])
@jwt_required()
def add_user_to_organisation(orgId):
    data = request.get_json()
    user_id_to_add = data.get('userId')

    if not user_id_to_add:
        return generate_error_response("userId is required", 422)

    current_user_id = get_jwt_identity()
    org = Organisation.query.get(orgId)
    current_user = User.query.get(current_user_id)
    user_to_add = User.query.get(user_id_to_add)

    if not org:
        return generate_error_response("Organisation not found", 404)

    if org.creator_id != uuid.UUID(current_user_id):
        return generate_error_response("Access forbidden", 403)

    if not user_to_add:
        return generate_error_response("User not found", 404)

    org.members.append(user_to_add)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User added to organisation successfully",
    }), 200
