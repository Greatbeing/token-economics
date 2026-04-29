#!/bin/bash
#
# 唯识进化引擎API服务管理脚本
#
# 用法:
#   ./manage.sh start   - 启动服务
#   ./manage.sh stop    - 停止服务
#   ./manage.sh restart - 重启服务
#   ./manage.sh status  - 查看服务状态
#   ./manage.sh log     - 查看日志

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR" || exit 1

PID_FILE="./api/api.pid"
LOG_FILE="./api/api.log"

# 启动服务
start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "服务已在运行 (PID: $PID)"
            return 1
        fi
    fi
    
    echo "启动唯识进化引擎API..."
    export PYTHONPATH="${PWD}:${PYTHONPATH}"
    
    nohup python3 -m uvicorn api.main:app \
        --host 0.0.0.0 \
        --port 8080 \
        --log-level info \
        > "$LOG_FILE" 2>&1 &
    
    echo $! > "$PID_FILE"
    sleep 2
    
    if kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "服务启动成功 (PID: $(cat "$PID_FILE"))"
        echo "API地址: http://0.0.0.0:8080"
    else
        echo "服务启动失败，请查看日志: $LOG_FILE"
        return 1
    fi
}

# 停止服务
stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "停止服务 (PID: $PID)..."
            kill "$PID"
            rm -f "$PID_FILE"
            echo "服务已停止"
        else
            echo "服务未运行"
            rm -f "$PID_FILE"
        fi
    else
        # 尝试通过端口查找进程
        PID=$(lsof -t -i:8080 2>/dev/null)
        if [ -n "$PID" ]; then
            echo "停止服务 (PID: $PID)..."
            kill "$PID"
            echo "服务已停止"
        else
            echo "服务未运行"
        fi
    fi
}

# 查看状态
status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "服务运行中 (PID: $PID)"
            curl -s http://localhost:8080/ 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print('服务:', d.get('service', 'unknown'))
    print('版本:', d.get('version', 'unknown'))
    print('活跃用户:', d.get('active_users', 0))
except:
    pass
"
        else
            echo "PID文件存在但服务未运行"
        fi
    else
        PID=$(lsof -t -i:8080 2>/dev/null)
        if [ -n "$PID" ]; then
            echo "服务运行中 (PID: $PID，未使用PID文件)"
        else
            echo "服务未运行"
        fi
    fi
}

# 查看日志
log() {
    if [ -f "$LOG_FILE" ]; then
        tail -50 "$LOG_FILE"
    else
        echo "日志文件不存在"
    fi
}

# 主逻辑
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 1
        start
        ;;
    status)
        status
        ;;
    log)
        log
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status|log}"
        exit 1
        ;;
esac
