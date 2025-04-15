from flask import Blueprint, render_template, session, redirect, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/ping")
def ping():
    return jsonify({"message": "pong"}), 200

@main_bp.route("/user/<user_id>")
def user_page(user_id):
    # ✅ 可选：校验用户是否已登录
    if session.get("user_id") != user_id:
        return redirect("/")
    return render_template("user.html", user_id=user_id)
