# ======= 必须最先设置环境变量（优先级高于后续 import）=======
import os
os.environ["MPLCONFIGDIR"] = "./cache/.matplotlib"
os.makedirs("./cache/.matplotlib", exist_ok=True)  # 确保目录存在
os.environ["NO_PROXY"] = "dashscope.aliyuncs.com"  # 避免 dashscope 请求被代理干扰

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # 或 logging.CRITICAL 完全禁止

# ======= 导入 Flask 应用 =======
from app import create_app, socketio

app = create_app()

# ======= 启动入口 =======
if __name__ == '__main__':
    print("✅ 正在启动 Flask SocketIO 服务...", flush=True)
    socketio.run(app, host='0.0.0.0', port=80, debug=False, log_output=False, allow_unsafe_werkzeug=True)
