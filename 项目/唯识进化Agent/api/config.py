# -*- coding: utf-8 -*-
"""
API配置文件
"""

import os

# 服务配置
HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", "5000"))

# 数据目录
DATA_DIR = os.getenv("DATA_DIR", "./data/users")

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Agent配置
AGENT_CONFIG_PATH = "./config/default.yaml"
AGENT_NAME_PREFIX = "Alaya_"

# 用户会话配置
MAX_CONTEXT_LENGTH = 10  # 保留最近N轮对话作为上下文
