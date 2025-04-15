from flask_socketio import SocketIO

def init_socketio(socketio: SocketIO):
    @socketio.on("join", namespace="/updates")
    def handle_join(user_id):
        print(f"✅ 用户 {user_id} 已加入 WebSocket 频道 /updates")
