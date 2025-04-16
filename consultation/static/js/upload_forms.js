let selectedFiles = [];

document.getElementById("fileInput").addEventListener("change", function () {
    const files = Array.from(this.files);
    const totalFiles = selectedFiles.length + files.length;

    if (totalFiles > 3) {
        alert("最多只能上传 3 张图片！");
        const allowedFiles = files.slice(0, 3 - selectedFiles.length);
        selectedFiles = [...selectedFiles, ...allowedFiles];
        this.files = new FileListItems([...selectedFiles]);
        updatePreview();
        return;
    }

    selectedFiles = [...selectedFiles, ...files];
    updatePreview();
});

function updatePreview() {
    const preview = document.querySelector(".preview");
    preview.innerHTML = "";

    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function (e) {
            const div = document.createElement("div");
            div.classList.add("image-container");

            const img = document.createElement("img");
            img.src = e.target.result;

            const btn = document.createElement("button");
            btn.innerText = "×";
            btn.classList.add("delete-btn");
            btn.onclick = () => removeImage(index);

            div.appendChild(img);
            div.appendChild(btn);
            preview.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}

function removeImage(index) {
    selectedFiles.splice(index, 1);
    updatePreview();
}

document.getElementById("uploadForm").addEventListener("submit", function (event) {
    event.preventDefault();

    if (selectedFiles.length === 0) {
        alert("请选择文件！");
        return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append("files", file);
    });

    fetch("/consultation/upload_images/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    }).then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("message").innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 2000);
            }
        }).catch(error => console.error("上传失败", error));
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function FileListItems(files) {
    let b = files || [];
    b.item = function (i) {
        return this[i];
    };
    return b;
}


function showSection(sectionId) {
    // 隐藏所有页面内 .content > div 的内容区域（你可以根据需要改类名）
    document.querySelectorAll('.content > div').forEach(div => {
        div.classList.add('hidden'); // 或 div.style.display = "none";
    });

    // 显示目标 section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('hidden'); // 或 section.style.display = "block";
    }
}

