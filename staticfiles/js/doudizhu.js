const socket = new WebSocket("ws://" + window.location.host + "/ws/game/");

socket.onopen = function () {
    console.log("✅ WebSocket 连接成功");
};

socket.onerror = function (error) {
    console.error("❌ WebSocket 错误", error);
};

socket.onclose = function (event) {
    console.warn("⚠️ WebSocket 连接关闭", event);
};

// 当前用户的用户名（从服务器获取）
let currentUsername = null;

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);

    if (data.type === "joined") {
        currentUsername = data.username;
        document.getElementById("playerUsername").textContent = currentUsername;
    }

    if (data.type === "status") {
        document.getElementById("readyCount").textContent = data.ready_count;
    }

    if (data.type === "deal") {
        const container = document.getElementById("hand");
        container.innerHTML = "";
        data.hand.forEach(card => {
            const el = document.createElement("div");
            el.className = "card";
            el.textContent = card;
            container.appendChild(el);
        });
    }

    if (data.type === "play") {
        alert(`玩家 ${data.player} 出牌：${data.card}`);
    }
};

function sendReady() {
    socket.send(JSON.stringify({ type: "ready" }));
}


