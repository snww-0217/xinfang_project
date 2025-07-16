document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('carForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(this);

        fetch('/consultation/upload_used_car/', {
            method: 'POST',
            body: formData,
            credentials: 'include'  // 保留登录凭证（cookies）
        })
        .then(response => response.json())
        .then(data => {
            const msgDiv = document.getElementById('message');
            if (data.status === 'success') {
                msgDiv.style.color = 'green';
                msgDiv.innerText = '上传成功！车辆ID: ' + data.car_id;
                document.getElementById('carForm').reset();
            } else {
                msgDiv.style.color = 'red';
                msgDiv.innerText = '上传失败: ' + data.message;
            }
        })
        .catch(error => {
            console.error('请求出错：', error);
            document.getElementById('message').innerText = '网络错误，请重试';
        });
    });
});

