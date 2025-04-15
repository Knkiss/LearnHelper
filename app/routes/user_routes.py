from flask import Blueprint, request, jsonify, session
from app.services.user_service import (
    register_user, login_user, set_user_key, has_user_key
)

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user_id = data.get("user_id")
    password_hash = data.get("password")
    code = data.get("code")

    success, message = register_user(user_id, password_hash, code)
    if success:
        return jsonify({"success": True, "message": message})
    return jsonify({"error": message}), 400


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password_hash = data.get("password_hash")

    success, message = login_user(user_id, password_hash)
    if success:
        session["user_id"] = user_id
        return jsonify({"success": True})
    return jsonify({"success": False, "error": message}), 400


@user_bp.route("/key/set", methods=["POST"])
def set_key():
    data = request.get_json()
    user_id = data.get("user_id")
    key = data.get("key")

    success, message = set_user_key(user_id, key)
    if success:
        return jsonify({"message": message})
    return jsonify({"error": message}), 400


@user_bp.route("/key/status")
def key_status():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "缺少 user_id"}), 400
    return jsonify({"has_key": has_user_key(user_id)})
