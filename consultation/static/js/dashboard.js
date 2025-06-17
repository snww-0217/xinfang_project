function showSection(id) {
    document.querySelectorAll('.section').forEach(sec => sec.style.display = 'none');
    document.getElementById(id).style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const input = document.getElementById('imageInput');
    const preview = document.getElementById('imagePreview');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const file = input.files[0];
        if (!file) return alert("Please select a file.");

        const formData = new FormData();
        formData.append('image', file);

        // 假设上传接口为 /upload-image/
        fetch('/upload-image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                preview.innerHTML = `<img src="${data.url}" alt="Uploaded Image">`;
            } else {
                alert("Upload failed.");
            }
        })
        .catch(() => alert("Upload error."));
    });
});

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === 'csrftoken') return value;
    }
    return '';
}

