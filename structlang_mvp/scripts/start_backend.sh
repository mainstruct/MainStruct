#!/bin/bash

# 启动后端服务

cd "$(dirname "$0")/.."

echo "启动 StructLang 后端服务..."
echo "================================"

# 检查环境变量
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    echo "请复制 .env.example 为 .env 并配置 ANTHROPIC_API_KEY"
    exit 1
fi

# 启动FastAPI
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
