import hashlib
import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

import requests

default_server_url = "127.0.0.1:80"


def get_tmp_dir():
    """
    获取临时文件夹路径，始终位于主程序所在目录的 tmp/ 下。
    无论是调试还是打包运行，均保证 tmp/ 路径正确。
    """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe，使用可执行文件所在目录
        base = os.path.dirname(sys.executable)
    else:
        # 调试模式：使用主程序入口（main.py）所在目录
        base = os.path.dirname(os.path.abspath(sys.argv[0]))

    tmp_path = os.path.join(base, 'tmp')
    os.makedirs(tmp_path, exist_ok=True)
    return tmp_path

def try_login(user_id: str, password_hash: str, server_url: str) -> bool:
    try:
        res = requests.post(f"http://{server_url}/user/login", json={
            "user_id": user_id,
            "password_hash": password_hash
        }, timeout=5)
        data = res.json()
        return data.get("success", False)
    except Exception as e:
        messagebox.showerror("网络异常", f"无法连接服务器：{e}")
        return False

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_or_load_config():
    # 尝试读取本地配置
    CONFIG_PATH = os.path.join(get_tmp_dir(), "config.json")
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            user_id = data.get("user_id")
            password_hash = data.get("password_hash")
            server_url = data.get("server_url")
            if user_id and password_hash and server_url and try_login(user_id, password_hash, server_url):
                return user_id, server_url

    # 显示登录窗口
    def submit():
        uid = entry_user.get().strip()
        pwd = entry_pass.get().strip()
        url = entry_server.get().strip().rstrip("/")  # 移除末尾的 /，防止拼接错误

        if not uid or not pwd:
            messagebox.showwarning("提示", "账号和密码不能为空")
            return

        # 🔍 检查服务器连接
        try:
            ping_resp = requests.get(f"http://{url}/ping", timeout=2)
            if ping_resp.status_code != 200:
                raise Exception("Ping失败")
        except Exception as e:
            messagebox.showerror("连接失败", f"无法连接服务器：{url}\n请检查地址或网络")
            return

        # ✅ 登录验证
        h = hash_password(pwd)
        if try_login(uid, h, url):
            os.makedirs("tmp", exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump({"user_id": uid, "password_hash": h, "server_url": url}, f, ensure_ascii=False, indent=2)
            root.user_id = uid
            root.url = url
            root.destroy()
        else:
            messagebox.showerror("登录失败", "账号或密码错误")

    # 创建窗口
    root = tk.Tk()
    root.title("LearnHelper 登录")
    root.geometry("350x300")
    root.resizable(False, False)

    tk.Label(root, text="用户账号").pack(pady=(15, 2))
    entry_user = tk.Entry(root, width=28)
    entry_user.pack()

    tk.Label(root, text="用户密码").pack(pady=(10, 2))
    entry_pass = tk.Entry(root, show="*", width=28)
    entry_pass.pack()

    tk.Label(root, text="服务器地址（IP:端口）").pack(pady=(10, 2))
    entry_server = tk.Entry(root, width=28)
    entry_server.insert(0, default_server_url)  # 设置默认值
    entry_server.pack()

    tk.Button(root, text="登录", width=20, command=submit).pack(pady=15)

    root.user_id = None
    root.url = default_server_url
    root.mainloop()

    if not root.user_id:
        raise RuntimeError("登录失败或用户取消")
    return root.user_id, root.url
