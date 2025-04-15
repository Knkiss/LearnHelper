import logging
import sys
from app.utils.path_manager import LOG_FILE

# 清除 root logger 默认输出（防止重复打印）
logging.root.handlers.clear()

# 全局 formatter：控制台和文件共用
formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# 封装日志获取函数
def get_logger(name="server_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:  # 避免重复绑定 handler
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 文件输出
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# 默认导出一个 logger 实例
logger = get_logger()
