#!/bin/bash
set -e

# 获取版本号，默认用 latest
VERSION=${1:-latest}
echo "部署版本号：$VERSION"
# 拉取最新代码
git pull origin develop

# 停止旧容器
docker compose stop web

# 重新构建镜像，传递版本号
docker compose build --build-arg WEB_VERSION=$VERSION web

# 启动新容器，传递版本号
WEB_VERSION=$VERSION docker compose up -d --force-recreate web

# 等待 web 容器健康（最多 30 秒）
echo "等待 web 容器启动..."
for i in {1..30}; do
  if docker exec xinfang_web python manage.py showmigrations &> /dev/null; then
    echo "Web 容器已就绪，检查是否需要迁移..."
    
    # 检查是否有未应用的迁移
    UNAPPLIED_MIGRATIONS=$(docker exec xinfang_web python manage.py showmigrations --plan | grep '\[ \]')
    
    if [ -n "$UNAPPLIED_MIGRATIONS" ]; then
      echo "检测到数据库有更新，执行迁移..."
      docker exec xinfang_web python manage.py migrate
    else
      echo "数据库无需迁移，跳过。"
    fi
    break
  fi
  echo "等待中 ($i/30)..."
  sleep 1
done

# 显示容器状态
docker ps

echo "🚀 部署完成！版本：$VERSION"
