import os

# === 基础路径 ===
BASE_CACHE_DIR = "cache"
BASE_DATA_DIR = "data"

# === 日志路径 ===
LOG_DIR = os.path.join(BASE_CACHE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "server.log")

# === 上传图像路径 ===
UPLOAD_DIR = os.path.join(BASE_CACHE_DIR, "uploads")

# === 用户数据路径（data/user/）===
USER_DATA_DIR = os.path.join(BASE_DATA_DIR, "user")

# === 激活码路径 ===
ACTIVATION_FILE = os.path.join(BASE_DATA_DIR, "activation_codes.json")

# === 初始化所有目录 ===
def init_directories():
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    os.makedirs(BASE_DATA_DIR, exist_ok=True)
