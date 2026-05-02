from flask import Blueprint, request, jsonify, g
from app.services.auth_service import AuthService
from app.utils.jwt_utils import require_auth

auth_bp = Blueprint("auth", __name__)
service = AuthService()


@auth_bp.post("/register")
def register():
    result = service.register(request.get_json(silent=True) or {})
    return jsonify(result), 201


@auth_bp.post("/login")
def login():
    return jsonify(service.login(request.get_json(silent=True) or {})), 200


@auth_bp.get("/me")
@require_auth
def me():
    return jsonify({"user": g.current_user.to_dict()}), 200
