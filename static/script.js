// SEND MESSAGE
document.querySelector(".btn-send").addEventListener("click", sendMsg);

function sendMsg() {
    let input = document.getElementById("chat-input");
    let msg = input.value.trim();
    if (!msg) return;

    let chatBox = document.querySelector(".chat-box");

    chatBox.innerHTML += `
    <div class="message user-message">
        <div class="message-content">
            <p>${msg}</p>
            <span class="timestamp">${getTime()}</span>
        </div>
    </div>`;

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {

        if (data.error) {
            alert("Login required");
            return;
        }

        chatBox.innerHTML += `
        <div class="message bot-message">
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <p>${data.reply}</p>
                <span class="timestamp">${getTime()}</span>
            </div>
        </div>`;

        chatBox.scrollTop = chatBox.scrollHeight;
    });

    input.value = "";
}

// TIME
function getTime() {
    let now = new Date();
    return now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

// NEW CHAT
document.querySelector(".btn-new-chat").addEventListener("click", () => {
    document.querySelector(".chat-box").innerHTML = "";
});

// LOAD RECENT CHATS
window.onload = function () {
    fetch("/get_chats")
    .then(res => res.json())
    .then(data => {
        let list = document.querySelector(".history-list");

        if (!list) return;

        list.innerHTML = "";

        data.forEach(chat => {
            let item = document.createElement("li");
            item.innerHTML = `<i class="fa-solid fa-message"></i> ${chat.substring(0,30)}`;
            list.appendChild(item);
        });
    });
};

// PROFILE DROPDOWN
function toggleMenu() {
    let menu = document.getElementById("profileDropdown");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

window.onclick = function(e) {
    if (!e.target.matches('.profile-icon')) {
        let menu = document.getElementById("profileDropdown");
        if (menu) menu.style.display = "none";
    }
};

document.addEventListener("DOMContentLoaded", function() {
    let t = document.getElementById("init-time");
    if (t) t.innerText = getTime();
});

document.querySelector(".btn-clear-history")?.addEventListener("click", () => {
    fetch("/clear_chats", { method: "POST" })
    .then(() => {
        document.querySelector(".history-list").innerHTML = "";
    });
});