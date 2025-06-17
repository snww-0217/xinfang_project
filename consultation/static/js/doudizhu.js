// doudizhu.js

let socket = null;
let currentUsername = null;

/**
 * 建立 WebSocket 连接
 */
function connectWebSocket() {
    socket = new WebSocket(`ws://${window.location.host}/ws/game/`);

    socket.onopen = () => {
        console.log("✅ WebSocket 已连接");
    };

    socket.onerror = (error) => {
        console.error("❌ WebSocket 错误：", error);
    };

    socket.onclose = (event) => {
        console.warn("⚠️ WebSocket 连接关闭：", event);
        // 尝试重连
        setTimeout(() => {
            console.log("🔄 正在尝试重新连接 WebSocket...");
            connectWebSocket();
        }, 3000);
    };

    socket.onmessage = handleMessage;
}

/**
 * 处理收到的消息
 * @param {MessageEvent} e
 */
function handleMessage(e) {
    const data = JSON.parse(e.data);

    switch (data.type) {
        case "joined":
            currentUsername = data.username;
            updatePlayerUsername(currentUsername);
            break;

        case "status":
            updateReadyCount(data.ready_count);
            break;

        case "deal":
            renderHand(data.hand);
            break;

        case "play":
            alert(`🎮 玩家 ${data.player} 出牌：${data.card}`);
            break;

        default:
            console.warn("⚠️ 未知消息类型：", data);
            break;
    }
}

/**
 * 安全发送消息
 * @param {string} type 消息类型
 * @param {object} payload 消息数据（可选）
 */
function sendMessage(type, payload = {}) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const message = { type, ...payload };
        socket.send(JSON.stringify(message));
        console.log(`📤 发送消息:`, message);
    } else {
        alert("❌ WebSocket 未连接，消息发送失败");
    }
}

/**
 * 点击“准备”按钮调用此函数
 */
window.sendReady = function () {
    sendMessage("ready");
};

/**
 * 更新用户名显示
 */
function updatePlayerUsername(username) {
    const el = document.getElementById("playerUsername");
    if (el) {
        el.textContent = username;
    }
}

/**
 * 更新准备人数显示
 */
function updateReadyCount(count) {
    const el = document.getElementById("readyCount");
    if (el) {
        el.textContent = count;
    }
}

/**
 * 渲染发到的手牌
 */
function renderHand(cards) {
    const container = document.getElementById("hand");
    if (!container) return;

    container.innerHTML = "";
    cards.forEach(card => {
        const cardEl = document.createElement("div");
        cardEl.className = "card";

        if (card.includes("♥ ") || card.includes("♦ ")) {
            cardEl.classList.add("red");
        }

        cardEl.textContent = card;
        container.appendChild(cardEl);
    });
}

// 页面加载时初始化 WebSocket
document.addEventListener("DOMContentLoaded", connectWebSocket);

