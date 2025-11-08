#!/bin/bash

# 启动前端服务

cd "$(dirname "$0")/.."

echo "启动 StructLang 前端服务..."
echo "================================"

# 检查环境变量
if [ ! -f .env ]; then
    echo "⚠️  未找到 .env 文件"
    echo "请复制 .env.example 为 .env 并配置 API_BASE_URL"
    exit 1
fi

# 启动Streamlit
cd frontend
streamlit run app.py --server.port 8501
