let isInitial = true;
let lastUpdatedAt = 0;
const socket = io("/updates");

document.getElementById("displayUserId").innerText = userId;

// ----------------- UI 控制 -----------------

function toggleSettingsMenu() {
  const menu = document.getElementById("settingsMenu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function openSettingsDialog() {
  hideSettingsMenu();
  document.getElementById("settingsModal").style.display = "block";
}

function hideSettingsDialog() {
  document.getElementById("settingsModal").style.display = "none";

  if (isInitial) {
    fetch(`/user/key/status?user_id=${encodeURIComponent(userId)}`)
      .then(res => res.json())
      .then(data => {
        if (!data.has_key) {
          alert("您尚未设置 API KEY，将返回首页。");
          window.location.href = "/";
        }
      })
      .catch(() => {
        alert("无法检测 KEY 状态，返回首页");
        window.location.href = "/";
      });
  }
}

function hideSettingsMenu() {
  document.getElementById("settingsMenu").style.display = "none";
}

// ----------------- KEY 设置与检测 -----------------

async function checkKeyStatus() {
  try {
    const res = await fetch(`/user/key/status?user_id=${encodeURIComponent(userId)}`);
    const data = await res.json();

    if (data.has_key) {
      isInitial = false;
      document.getElementById("mainContent").style.display = "block";
    } else {
      document.getElementById("settingsModal").style.display = "block";
    }
  } catch {
    alert("网络错误，无法获取 KEY 状态！");
  }
}

async function submitSettings() {
  const key = document.getElementById("apiKeyInput").value.trim();
  if (!key) {
    alert("API Key 不能为空！");
    return;
  }

  const res = await fetch("/user/key/set", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, key: key })
  });

  const result = await res.json();
  alert(result.message || "保存成功！");
  isInitial = false;
  hideSettingsDialog();
  document.getElementById("mainContent").style.display = "block";
}

// ----------------- 图片更新 -----------------

function updateScreenshot() {
  const ts = Date.now();
  document.getElementById("screenshot").src = `/uploads/${userId}.png?ts=${ts}`;
}

// ----------------- WebSocket 实时监听 -----------------

socket.on("connect", () => {
  console.log("✅ Socket.IO 已连接");
  socket.emit("join", userId);
});

socket.on("disconnect", () => {
  console.warn("⚠️ Socket.IO 连接断开");
});

socket.on("update", (data) => {
  if (data.user_id === userId && data.timestamp > lastUpdatedAt) {
    lastUpdatedAt = data.timestamp;
    document.getElementById("status").innerText = data.status || "无状态";
    updateScreenshot();

    if (data.status?.includes("截图展示")) {
      document.getElementById("imageBlock").style.display = "block";
      document.getElementById("ocrBlock").style.display = "none";
      document.getElementById("answerBlock").style.display = "none";
      document.getElementById("errorBlock").style.display = "none";
    }

    if (data.status?.includes("回答完成")) {
      document.getElementById("ocrText").innerText = data.ocr || "";
      document.getElementById("answerText").innerText = data.answer || "";
      document.getElementById("ocrBlock").style.display = "block";
      document.getElementById("answerBlock").style.display = "block";
      document.getElementById("imageBlock").style.display = "block";
      document.getElementById("errorBlock").style.display = "none";
    }

    if (data.status?.includes("处理失败")) {
      document.getElementById("errorText").innerText = data.error || "未提供错误信息";
      document.getElementById("errorBlock").style.display = "block";
      document.getElementById("ocrBlock").style.display = "none";
      document.getElementById("answerBlock").style.display = "none";
    }
  }
});

// ----------------- 退出登录 -----------------

function logoutConfirm() {
  if (confirm("确定要退出登录吗？")) {
    fetch("/logout", { method: "POST" })
      .then(() => {
        window.location.href = "/";
      })
      .catch(() => {
        alert("退出失败，请重试");
      });
  }
}

// ----------------- 启动入口 -----------------

window.onload = checkKeyStatus;
