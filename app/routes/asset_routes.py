import os
from flask import Blueprint, send_from_directory
from app.utils.path_manager import UPLOAD_DIR

asset_bp = Blueprint("asset", __name__)

@asset_bp.route("/uploads/<filename>")
def serve_file(filename):
    abs_dir = os.path.abspath(UPLOAD_DIR)
    return send_from_directory(abs_dir, filename)
