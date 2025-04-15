import os
import json
from app.utils.path_manager import USER_DATA_DIR

def get_user_path(user_id):
    return os.path.join(USER_DATA_DIR, f"{user_id}.json")

def has_user(user_id):
    """判断用户是否存在"""
    return os.path.exists(get_user_path(user_id))

def load_user_data(user_id):
    """加载用户数据字典"""
    path = get_user_path(user_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(user_id, data):
    """保存用户数据字典"""
    path = get_user_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_key(user_id):
    """获取用户的 API Key"""
    user = load_user_data(user_id)
    if not user:
        return None
    return user.get("key")

def set_user_key(user_id, key):
    """设置用户的 API Key"""
    data = load_user_data(user_id) or {}
    data["key"] = key
    save_user_data(user_id, data)
