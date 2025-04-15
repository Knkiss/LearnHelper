import os
import io
import time
import base64
import numpy as np
from PIL import Image
from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor

from app import socketio, logger
from app.services.qa_service import process_image_ocr, process_image_no_ocr
from app.utils.account_utils import get_user_key, has_user
from app.utils.status_store import user_status, update_user_status, clear_user_error
from app.utils.path_manager import UPLOAD_DIR

qa_bp = Blueprint("qa", __name__, url_prefix="/qa")

executor = ThreadPoolExecutor(max_workers=10)

@qa_bp.route("/upload", methods=["POST"])
def upload_file():
    user_id = request.form.get("user_id")
    mode = request.form.get("mode", "full")
    file = request.files.get("file")

    if not user_id or not file:
        return jsonify({"error": "缺少 user_id 或截图文件"}), 400

    if not has_user(user_id):
        return jsonify({"error": "用户不存在"}), 404

    key = get_user_key(user_id)
    if not key:
        update_user_status(user_id, "❌ 上传失败", error="该用户未设置 API Key")
        return jsonify({"error": "该用户未设置 API Key"}), 403

    try:
        clear_user_error(user_id)
        update_user_status(user_id, "📥 收到截图，准备处理")

        save_path = os.path.join(UPLOAD_DIR, f"{user_id}.png")
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        img.save(save_path)
        logger.info(f"用户 {user_id} 上传截图，已保存为 {save_path}")

        # 模型调用分发
        from app.models.chat_model import ChatModel
        if mode == "show":
            update_user_status(user_id, "🖼️ 截图展示模式（数字键4）")
            return jsonify({"message": "截图上传成功，仅用于展示"}), 200

        elif mode == "text":
            img_np = np.array(img)
            model = ChatModel("qwen", key, "qwen-turbo")
            executor.submit(process_image_ocr, user_id, img_np, model)
            return jsonify({"message": "正在后台进行 OCR + 回答"}), 200

        elif mode == "image":
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            model = ChatModel("qwen", key, "qwen-vl-max")
            executor.submit(process_image_no_ocr, user_id, img_base64, model)
            return jsonify({"message": "正在后台进行图像问答"}), 200

        else:
            return jsonify({"error": "无效的 mode 参数"}), 400

    except Exception as e:
        logger.exception("上传处理异常")
        update_user_status(user_id, "❌ 上传失败", error=str(e))
        return jsonify({"error": str(e)}), 500
