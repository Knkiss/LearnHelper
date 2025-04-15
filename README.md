# LearnHelper

**LearnHelper** 是一个基于 Flask + SocketIO 构建的客户端+网页端+后端服务，支持图像上传、OCR 识别、多模态问答、用户注册登录及实时交互。适用于学习辅助场景。

---

## 🔧 功能模块

- 📸 **截图上传**：客户端通过 `/qa/upload` 接口上传图像
- 🧠 **问答系统**：
  - 文本问答（OCR + Qwen Turbo）
  - 图像问答（Qwen VL Max）
- 🔐 **用户系统**：
  - 注册、登录（密码加密存储）
  - 支持设置 API Key
- 🔁 **实时状态反馈**：Socket.IO 实时推送任务状态与结果
- 📦 **本地资源管理**：上传图像、日志、用户数据分类存储

---

## 📁 项目结构

```
LearnHelper/
│
├── main.py                   # 启动主程序
├── run.bat                   # 一键启动脚本
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖说明
├── .gitignore
│
├── app/                      # 服务端主模块
│   ├── __init__.py           # Flask 创建入口
│   ├── websocket.py          # WebSocket 事件处理器
│   ├── models/               # 模型模块（OCR、Chat）
│   │   ├── chat_model.py
│   │   ├── ocr_model.py
│   ├── routes/               # Flask 路由蓝图
│   │   ├── asset_routes.py
│   │   ├── main_routes.py
│   │   ├── qa_routes.py
│   │   ├── user_routes.py
│   ├── services/             # 核心业务逻辑
│   │   ├── qa_service.py
│   │   ├── user_service.py
│   ├── utils/                # 工具模块
│   │   ├── logger.py
│   │   ├── account_utils.py
│   │   ├── path_manager.py
│   │   ├── status_store.py
│   ├── static/               # 前端静态资源
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── templates/            # 前端 HTML 模板
│       ├── index.html
│       └── user.html
│
├── client/                   # 客户端项目（Tkinter GUI）
│   ├── build.bat             # 打包脚本
│   ├── icon.ico              # 客户端图标
│   ├── main.py               # 客户端入口
│   ├── requirements.txt      # 客户端依赖（requests + tkinter）
│   └── code/                 # 客户端模块逻辑
│       ├── uploader.py       # 上传功能
│       ├── logger.py         # 日志输出
│       ├── utils.py          # 工具函数
│       └── __init__.py
```

---

## 🚀 快速开始

### 1️⃣ 安装依赖（服务端）

在根目录下运行：

```bash
pip install -r requirements.txt
```

---

### 2️⃣ 启动服务端

确保当前目录为 `LearnHelper/`，然后运行：

```bash
python main.py
```

成功启动后，后端会监听默认的 `http://localhost:80` 地址。

---

### 3️⃣ 网页端注册与登录

在浏览器中访问服务地址：

- 📥 访问注册 & 登录页：`http://localhost/`
- 🔑 注册时需输入邀请码（激活码）
- ✅ 登录成功后跳转个人页面：`http://localhost/user/<user_id>`

> ⚠️ 注意：用户注册应先于客户端登录。

---

### 4️⃣ 启动客户端（桌面端）

进入 `client/` 目录后，运行客户端主程序：

```bash
python main.py
```

首次启动客户端时，你需要输入：

- ✅ 用户账号 & 密码  
- 🌐 服务器地址（例如：`localhost:80` 或云服务器 IP）  

客户端会尝试连接服务端并登录，成功后自动保存配置。

> ⚠️ 也可选择运行build.bat进行打包后运行.exe文件
---

### 📱 使用建议：网页 + 客户端协同操作

- 🖥️ **电脑端**：使用客户端登录，支持快捷截图并上传
- 📱 **移动设备端**：登录网页端实时查看截图内容、大模型回答和错误信息反馈
- 🧠 推荐在一台电脑上后台运行客户端，使用访问网页查看实时结果

---

## 📬 联系与许可

本项目仅供学习用途，严禁传播、倒卖或用于任何违法用途。