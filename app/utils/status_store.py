import time
from app import socketio

# 所有用户的状态
user_status = {}

def update_user_status(user_id, status, error=None):
    user_status.setdefault(user_id, {
        "ocr": "",
        "answer": "",
        "status": "",
        "error": "",
        "updated_at": 0
    })

    user_status[user_id]["status"] = status
    user_status[user_id]["updated_at"] = time.time()
    if error is not None:
        user_status[user_id]["error"] = error

    emit_status(user_id)

def clear_user_error(user_id):
    user_status.setdefault(user_id, {})
    user_status[user_id]["error"] = ""

def emit_status(user_id):
    socketio.emit("update", {
        "user_id": user_id,
        "timestamp": time.time(),
        "status": user_status[user_id].get("status", ""),
        "ocr": user_status[user_id].get("ocr", ""),
        "answer": user_status[user_id].get("answer", ""),
        "error": user_status[user_id].get("error", "")
    }, namespace="/updates")
