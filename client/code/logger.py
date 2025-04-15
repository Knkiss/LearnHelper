import logging
import os
from code.utils import get_tmp_dir

# 日志文件路径
log_file_path = os.path.join(get_tmp_dir(), "client.log")

# 创建 logger
logger = logging.getLogger("client_logger")
logger.setLevel(logging.INFO)

# 控制台 handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 文件 handler
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.INFO)

# 日志格式
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
