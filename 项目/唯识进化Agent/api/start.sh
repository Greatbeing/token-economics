#!/bin/bash
# 唯识进化引擎API启动脚本

cd "$(dirname "$0")/.." || exit 1

# 设置环境变量
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# 默认配置
HOST=${API_HOST:-"0.0.0.0"}
PORT=${API_PORT:-5000}
LOG_LEVEL=${LOG_LEVEL:-"info"}

echo "=========================================="
echo "  唯识进化引擎API启动中..."
echo "  监听地址: ${HOST}:${PORT}"
echo "=========================================="

# 启动服务
python3 -m uvicorn api.main:app \
    --host "${HOST}" \
    --port "${PORT}" \
    --log-level "${LOG_LEVEL}" \
    --reload
