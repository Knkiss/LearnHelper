from flask import Flask
from flask_socketio import SocketIO

from app.utils.path_manager import init_directories
init_directories()

from app.utils.logger import logger

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "BaiYuLong"

    # 注册蓝图
    from app.routes.main_routes import main_bp
    from app.routes.qa_routes import qa_bp
    from app.routes.user_routes import user_bp
    from app.routes.asset_routes import asset_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(qa_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(asset_bp)

    # 初始化 socketio
    from app.websocket import init_socketio
    init_socketio(socketio)

    socketio.init_app(app)
    return app
