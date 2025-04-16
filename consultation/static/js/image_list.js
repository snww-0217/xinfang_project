window.onload = function() {
    // 显示图片的函数
    window.showImage = function(imageUrl) {
        const modal = document.getElementById('image-modal');
        const modalImage = document.getElementById('modal-image');
        modalImage.src = imageUrl;
        modal.classList.add('active');
    };

    // 关闭放大图片的模态框
    window.closeModal = function() {
        document.getElementById('image-modal').classList.remove('active');
    };

    // 删除图片的函数
    window.deleteImage = function(imageId) {
        if (!confirm("确认删除这张图片？")) return;

        fetch(`/consultation/delete_image/${imageId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: `image_id=${imageId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "图片删除成功") {
                const li = document.getElementById(`image-${imageId}`);
                if (li) li.remove();
                alert("删除成功");
            } else {
                alert("删除失败: " + (data.error || "未知错误"));
            }
        })
        .catch(error => {
            console.error("删除请求失败:", error);
            alert("删除请求出错");
        });
    };

    // 分页切换
    window.changePage = function(pageNumber) {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('page', pageNumber);
        window.location.href = currentUrl.toString();
    };

    // 获取 CSRF Token
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
};

