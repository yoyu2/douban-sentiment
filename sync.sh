#!/bin/bash
set -e

# =========================
# 同步到阿里云 ECS 脚本
# =========================

ECS_IP="47.113.193.26"
ECS_USER="root"
ECS_PATH="/opt/douban-sentiment-project"

echo "========================================"
echo "  同步项目到 ECS: ${ECS_IP}"
echo "========================================"

# 1. 构建前端
echo ""
echo "[1/3] 构建前端..."
cd "$(dirname "$0")/frontend"
npm run build
cd ..

# 2. 同步代码
echo ""
echo "[2/3] 同步代码到 ECS..."
rsync -avz \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude 'frontend/node_modules' \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude 'data/' \
  --delete \
  ./ "${ECS_USER}@${ECS_IP}:${ECS_PATH}/"

# 3. 重启后端 + 重载 nginx
echo ""
echo "[3/3] 重启 ECS 上的后端和 nginx..."
ssh "${ECS_USER}@${ECS_IP}" << 'REMOTE'
  sudo systemctl restart douban-api
  echo "后端已重启 ($(sudo systemctl is-active douban-api))"

  sudo nginx -s reload
  echo "nginx 已重载"
REMOTE

echo ""
echo "========================================"
echo "  同步完成"
echo "  http://${ECS_IP}"
echo "========================================"
