FROM python:3.9-slim
# 更新包列表并安装 curl 和 netcat 工具
RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \  
    libmariadb-dev \
    build-essential \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置 Rust 镜像源
RUN export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static \
    && export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y
 
RUN apt-get update && apt-get install -y vim

ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将整个项目复制到镜像中
COPY . .

# 设置环境变量，告知 Django 以开发模式运行，禁止 Python 输出缓冲
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=xinfang_project.settings

# 设置端口
EXPOSE 8000

# 运行 Django 的开发服务器
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# daphne 启动 ASGI 应用，端口 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "xinfang_project.asgi:application"]

