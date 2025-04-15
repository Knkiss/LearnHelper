import json
from app.utils.account_utils import (
    has_user, load_user_data, save_user_data,
    get_user_key, set_user_key as save_key
)
from app.utils.path_manager import ACTIVATION_FILE
from app import logger

def register_user(user_id, password_hash, code):
    if not user_id or not password_hash or not code:
        return False, "缺少参数"

    if has_user(user_id):
        return False, "该用户已存在"

    try:
        with open(ACTIVATION_FILE, "r", encoding="utf-8") as f:
            codes = json.load(f)
        if code not in codes["codes"]:
            return False, "激活码无效"

        # 移除激活码
        codes["codes"].remove(code)
        with open(ACTIVATION_FILE, "w", encoding="utf-8") as f:
            json.dump(codes, f, indent=2, ensure_ascii=False)

        save_user_data(user_id, {"password_hash": password_hash})
        return True, "注册成功"

    except Exception as e:
        logger.exception("注册失败")
        return False, str(e)


def login_user(user_id, password_hash):
    if not has_user(user_id):
        return False, "用户不存在"

    data = load_user_data(user_id)
    if data.get("password_hash") != password_hash:
        return False, "密码错误"

    return True, "登录成功"


def set_user_key(user_id, key):
    if not has_user(user_id):
        return False, "用户不存在"
    save_key(user_id, key)
    return True, "Key 保存成功"


def has_user_key(user_id):
    key = get_user_key(user_id)
    return bool(key)
