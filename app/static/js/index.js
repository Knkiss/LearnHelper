// 引入 SHA-256 加密（使用 Web Crypto API）
function hashPassword(password) {
  return sha256(password);
}

// 登录请求（加密后提交）
async function login() {
  const userId = document.getElementById("userIdInput").value.trim();
  const password = document.getElementById("passwordInput").value.trim();

  if (!userId || !password) {
    alert("请输入账号和密码！");
    return;
  }

  const hashedPassword = await hashPassword(password);

  fetch("/user/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, password_hash: hashedPassword })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.href = `/user/${encodeURIComponent(userId)}`;
      } else {
        alert(data.error || "登录失败");
      }
    })
    .catch(err => {
      alert("网络错误：" + err);
    });
}

function showModal() {
  document.getElementById("activationModal").style.display = "flex";
}

function hideModal() {
  document.getElementById("activationModal").style.display = "none";
}

// 注册请求（加密后提交）
async function submitActivation() {
  const code = document.getElementById("activationCodeInput").value.trim();
  const userId = document.getElementById("userIdInput").value.trim();
  const password = document.getElementById("passwordInput").value.trim();

  if (!userId || !password) {
    alert("请输入账号和密码！");
    return;
  }

  if (!code) {
    alert("请输入激活码！");
    return;
  }

  const hashedPassword = await hashPassword(password);

  fetch("/user/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      password: hashedPassword,
      code: code
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert("注册成功，请登录");
        hideModal();
      } else {
        alert(data.error || "注册失败");
      }
    })
    .catch(err => {
      alert("网络错误：" + err);
    });
}


document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("activationModal");

  // 点击遮罩空白部分关闭弹窗
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      hideModal();
    }
  });
});
